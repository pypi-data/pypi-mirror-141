"""
Primary class for performing the parameter fitting in KIPET

"""
# Standard library imports
import copy
import os
import time
import warnings

# Third party imports
import numpy as np
import pandas as pd
from pyomo.environ import (Constraint, ConstraintList, Objective,
    SolverFactory, Suffix, TerminationCondition, value, Var)
from scipy.sparse import coo_matrix
import scipy.stats as st

# KIPET library imports
from kipet.model_components.objectives import (comp_objective,
                                               conc_objective)
from kipet.input_output.read_hessian import split_sipopt_string, read_reduce_hessian, save_eig_red_hess
from kipet.estimator_tools.pyomo_simulator import PyomoSimulator
from kipet.estimator_tools.results_object import ResultsObject
from kipet.mixins.parameter_estimator_mixins import PEMixins
from kipet.model_tools.pyomo_model_tools import convert
from kipet.general_settings.variable_names import VariableNames


class ParameterEstimator(PEMixins, PyomoSimulator):

    """Optimizer for parameter estimation"""

    def __init__(self, model):
        super(ParameterEstimator, self).__init__(model)

        self.__var = VariableNames()

        self.hessian = None
        self.cov = None
        self._estimability = False
        self._idx_to_variable = dict()
        self._n_actual = self._n_components
        self.model_variance = True
        self.termination_condition = None
        
        # This should be a subclass or a mixin
        self.G_contribution = None
        self.unwanted_G = False
        self.time_variant_G = False
        self.time_invariant_G = False
        self.time_invariant_G_decompose = False
        self.time_invariant_G_no_decompose = False
        
        # Parameter name list
        self.param_names = []
        self.param_names_full = [f'P[{p}]' for p in getattr(self.model, self.__var.model_parameter)]
        self.param_names = [p for p in getattr(self.model, 'P')]
        if hasattr(self.model, 'Pinit'):
            self.param_names_full += [f'init_conditions[{p}]' for p in getattr(self.model, 'Pinit')]
            self.param_names += [p for p in getattr(self.model, 'Pinit')]

        if hasattr(self.model, 'non_absorbing'):
            warnings.warn("Overriden by non_absorbing")
            list_components = [k for k in self._mixture_components if k not in self._non_absorbing]
            self._sublist_components = list_components
            self._n_actual = len(self._sublist_components)

        # for new huplc structure (CS):
        if self._huplc_given:
            self._list_huplcabs = self._huplc_absorbing
            # self._n_huplc = len(self._list_huplcabs)

        if hasattr(self.model, 'known_absorbance'):
            warnings.warn("Overriden by known_absorbance")
            list_components = [k for k in self._mixture_components if k not in self._known_absorbance]
            self._sublist_components = list_components
            self._n_actual = len(self._sublist_components)

        else:
            self._sublist_components = [k for k in self._mixture_components]
            
        if hasattr(self, '_abs_components'):
            self.component_set = self._abs_components
            self.component_var = self.__var.concentration_spectra_abs
            self.n_val = self._nabs_components
            
        else:
            self.component_set = self._sublist_components
            self.component_var = self.__var.concentration_spectra
            self.n_val = self._n_actual
            
    def run_opt(self, solver, **kwds):

        """ Solves parameter estimation problem.

        :param str solver: The solver used to solve the NLP
        :param dict kwds: The dictionary of options passed from the ReactionModel

        :Keyword Args:
            - solver (str): name of the nonlinear solver to used
            - solver_opts (dict, optional): options passed to the nonlinear solver
            - variances (dict or float, optional): map of component name to noise variance. The
              map also contains the device noise variance. If not float then we only use device variance
              and ignore model variance.
            - tee (bool,optional): flag to tell the optimizer whether to stream output
              to the terminal or not.
            - with_d_vars (bool,optional): flag to the optimizer whether to add
            - variables and constraints for D_bar(i,j).
            - report_time (bool, optional): flag as to whether to time the parameter estimation or not.
            - estimability (bool, optional): flag to tell the model whether it is
              being used by the estimability analysis and therefore will need to return the
              hessian for analysis.
            - model_variance (bool, optional): Default is True. Flag to tell whether we are only
              considering the variance in the device, or also model noise as well.
            - model_variance (bool, optional): Default is True. Flag to tell whether we are only
              considering the variance in the device, or also model noise as well.

        :return: The results from the parameter fitting
        :rtype: ResultsObject

        """
        run_opt_kwargs = copy.copy(kwds)
        
        solver_opts = kwds.pop('solver_opts', dict())
        variances = kwds.pop('variances', dict())
        tee = kwds.pop('tee', False)
        with_d_vars = kwds.pop('with_d_vars', False)
        covariance = kwds.pop('covariance', False)
 
        estimability = kwds.pop('estimability', False)
        report_time = kwds.pop('report_time', False)
        model_variance = kwds.pop('model_variance', True)

        inputs_sub = kwds.pop("inputs_sub", None)
        trajectories = kwds.pop("trajectories", None)
        fixedtraj = kwds.pop("fixedtraj", False)
        fixedy = kwds.pop("fixedy", False)
        yfix = kwds.pop("yfix", None)
        yfixtraj = kwds.pop("yfixtraj", None)

        jump = kwds.pop("jump", False)
        
        self.confidence = kwds.pop('confidence', None)
        if self.confidence is None:
            self.confidence = 0.95
        
        G_contribution = kwds.pop('G_contribution', None)
        St = kwds.pop('St', dict())
        Z_in = kwds.pop('Z_in', dict())

        self.solver = solver
        self.model_variance = model_variance
        self._estimability = estimability

        if not self.model.alltime.get_discretization_info():
            raise RuntimeError('apply discretization first before initializing')

        self.G_contribution = G_contribution
       
        if report_time:
            start = time.time()

        opt = SolverFactory(self.solver)
        
        if self.G_contribution == 'time_invariant_G':
            self.decompose_G_test(St, Z_in)
        self.g_handling_status_messages()

        if covariance:
            if self.solver != 'ipopt_sens' and self.solver != 'k_aug':
                raise RuntimeError('To get covariance matrix the solver needs to be ipopt_sens or k_aug')
            
            if self.solver == 'ipopt_sens':
                if not 'compute_red_hessian' in solver_opts.keys():
                    solver_opts['compute_red_hessian'] = 'yes'
            
            if self.solver == 'k_aug':
                solver_opts['compute_inv'] = ''

            self._define_reduce_hess_order()

        if inputs_sub is not None:
            from kipet.estimator_tools.additional_inputs import add_inputs
            
            add_kwargs = dict(
                fixedtraj = fixedtraj,
                fixedy = fixedy, 
                inputs_sub = inputs_sub,
                yfix = yfix,
                yfixtraj = yfixtraj,
                trajectories = trajectories,
            )
            add_inputs(self, add_kwargs)
        
        if jump:
            from kipet.estimator_tools.jumps_method import set_up_jumps
            set_up_jumps(self.model, run_opt_kwargs)
            
        for key, val in solver_opts.items():
            opt.options[key] = val
            
        self.objective_value = 0
        active_objectives = [o for o in self.model.component_map(Objective, active=True)]        
        if active_objectives:
            print(
                "WARNING: The model has an active objective. Running optimization with models objective.\n"
                " To solve optimization with default objective (Weifengs) deactivate all objectives in the model.")
            solver_results = opt.solve(self.model, tee=tee)

        elif self._spectra_given:
            self.objective_value, self.cov_mat = self._solve_extended_model(
                variances, 
                opt,
                tee=tee,
                covariance=covariance,
                with_d_vars=with_d_vars,
                **kwds)

        elif self._concentration_given:
            self.objective_value, self.cov_mat = self._solve_model_given_c(
                variances, 
                opt,
                tee=tee,
                covariance=covariance,
                **kwds)
       
        else:
            raise RuntimeError(
                'Must either provide concentration data or spectra in order to solve the parameter estimation problem')

        if report_time:
            end = time.time()
            print("Total execution time in seconds for variance estimation:", end - start)

        return self._get_results()

    def _get_results(self):
        """Removed results unit from function

        :return: The formatted results
        :rtype: ResultsObject

        """
        results = ResultsObject()
        results.objective = self.objective_value
        results.parameter_covariance = self.cov
        results.load_from_pyomo_model(self.model)
        results.show_parameters(self.confidence)

        if self._spectra_given:
            from kipet.calculation_tools.beer_lambert import D_from_SC
            D_from_SC(self.model, results)

        if hasattr(self.model, self.__var.model_parameter_scaled): 
            setattr(results, self.__var.model_parameter, {name: getattr(self.model, self.__var.model_parameter)[name].value*getattr(self.model, self.__var.model_parameter_scaled)[name].value for name in self.model.parameter_names})
        else:
            setattr(results, self.__var.model_parameter, {name: getattr(self.model, self.__var.model_parameter)[name].value for name in self.model.parameter_names})

        if self.termination_condition!=None and self.termination_condition!=TerminationCondition.optimal:
            raise Exception("The current iteration was unsuccessful.")
        else:
            if self._estimability == True:
                return self.hessian, results
            else:
                return results

        return results

    def _get_list_components(self, species_list):
        """Returns the list of components used

        :param list species_list: List of species

        :return: List of model components
        :rtype: list

        """
        if species_list is None:
            list_components = [k for k in self._mixture_components]
        else:
            list_components = []
            for k in species_list:
                if k in self._mixture_components:
                    list_components.append(k)
                else:
                    warnings.warn("Ignored {} since is not a mixture component of the model".format(k))

        return list_components
            
    def _get_objective_expr(self, model, with_d_vars, component_set, sigma_sq, device=False):
        """Build the objective expression for D_bar (primary objective term in KIPET)

        :param ConcreteModel model: The model for use in parameter fitting
        :param bool with_d_vars: For spectral problems
        :param list component_set: A list of the components
        :param dict sigma_sq: A dictionary of component variances
        :param bool device: Indicates if the device variance is used

        :return expr: The objective expression
        :rtype: expression

        """
        expr = 0
        for t in model.times_spectral:
            for l in model.meas_lambdas:
                
                #print(t, l)
                if with_d_vars:
                #    print('Here 1')
                    D_bar = model.D_bar[t, l]
                else:
                    if device:    
                        if hasattr(model, 'huplc_absorbing'):
                #            print('Here 2')
                            D_bar = sum(model.Z[t, k] * model.S[l, k] for k in component_set if k not in model.solid_spec_arg1)
                        else:
                #            print('Here 3')
                            D_bar = sum(model.Z[t, k] * model.S[l, k] for k in component_set)    
                    else:
                        if hasattr(model, '_abs_components'):
                            if hasattr(model, 'huplc_absorbing') and hasattr(model, 'solid_spec_arg1'):
                #                print('Here 4')
                                D_bar = sum(model.Cs[t, k] * model.S[l, k] for k in model._abs_components if k not in model.solid_spec_arg1)
                            else:
                #                print('Here 5')
                                D_bar = sum(model.Cs[t, k] * model.S[l, k] for k in model._abs_components)
                        else:
                            if hasattr(model, 'huplc_absorbing') and hasattr(model, 'solid_spec_arg1'):
                #                print('Here 6')
                                D_bar = sum(model.C[t, k] * model.S[l, k] for k in component_set if k not in model.solid_spec_arg1)
                            else:
                #                print('Here 7')
                                D_bar = sum(model.C[t, k] * model.S[l, k] for k in component_set)
                
                #print(D_bar)
                            
                if self.G_contribution == 'time_variant_G':
                    expr += (model.D[t, l] - D_bar - model.qr[t]*model.g[l]) ** 2 / (sigma_sq['device'])
                elif self.time_invariant_G_no_decompose:
                    expr += (model.D[t, l] - D_bar - model.g[l]) ** 2 / (sigma_sq['device'])
                else:
                    expr += (model.D[t, l] - D_bar) ** 2 / (sigma_sq['device'])
                   
        #print(expr) 
                   
        return expr 

    def _solve_extended_model(self, sigma_sq, optimizer, **kwds):
        """Solves estimation based on spectral data. (known variances)

           This method is not intended to be used by users directly

        :param dict sigma_sq: variances
        :param SolverFactory optimizer: Pyomo Solver factory object

        :Keyword Args:

            - tee (bool,optional): flag to tell the optimizer whether to stream output
              to the terminal or not
            - with_d_vars (bool,optional): flag to the optimizer whether to add
              variables and constraints for D_bar(i,j)
            - subset_lambdas (array_like,optional): Set of wavelengths to used in
              the optimization problem (not yet fully implemented). Default all wavelengths.

        :return: None

        """
        tee = kwds.pop('tee', False)
        with_d_vars = kwds.pop('with_d_vars', False)

        if self._huplc_given:  # added for new huplc structure CS
            weights = kwds.pop('weights', [1.0, 1.0, 1.0])
        else:
            weights = kwds.pop('weights', [1.0, 1.0])
        warmstart = kwds.pop('warmstart', False)
        eigredhess2file = kwds.pop('eigredhess2file', False)
        penaltyparam = kwds.pop('penaltyparam', False)
        penaltyparamcon = kwds.pop('penaltyparamcon', False) #added for optional penalty term related to constraint CS
        ppenalty_dict = kwds.pop('ppenalty_dict', None)
        ppenalty_weights = kwds.pop('ppenalty_weights', None)
        covariance = kwds.pop('covariance', False)
        species_list = kwds.pop('subset_components', None)
        set_A = kwds.pop('subset_lambdas', list())
        
        self._eigredhess2file=eigredhess2file
        cov_mat = None

        if not set_A:
            set_A = self.model.meas_lambdas

        list_components = self._get_list_components(species_list)
        
        if not self._spectra_given:
            raise NotImplementedError("Extended model requires spectral data model.D[ti,lj]")

        if hasattr(self.model, 'non_absorbing'):
            warnings.warn("Overriden by non_absorbing!")
            list_components = [k for k in self._mixture_components if k not in self._non_absorbing]

        if hasattr(self.model, 'known_absorbance'):
            warnings.warn("Overriden by known_absorbance!")
            list_components = [k for k in self._mixture_components if k not in self._known_absorbance]

        all_sigma_specified = True

        if isinstance(sigma_sq, dict): 
            keys = sigma_sq.keys()
            for k in list_components:
                if k not in keys:
                    all_sigma_specified = False
                    sigma_sq[k] = max(sigma_sq.values())

            if not 'device' in sigma_sq.keys():
                all_sigma_specified = False
                sigma_sq['device'] = 1.0

        elif isinstance(sigma_sq, float):
            sigma_dev = sigma_sq
            sigma_sq = dict()
            sigma_sq['device'] = sigma_dev

        model = self.model
        
        # Instead of calling (19), (24) is called but all qr[i] are fixed at 1.0. KH.L
        if self.time_invariant_G_no_decompose:
            for i in model.times_spectral:
                model.qr[i] = 1.0
            model.qr.fix()

        def _qr_end_constraint(model):
            return model.qr[model.times_spectral[-1]] == 1.0
        
        if self.G_contribution == 'time_variant_G':
            model.qr_end_cons = Constraint(rule = _qr_end_constraint)
        
        
        if with_d_vars and self.model_variance:
            model.D_bar = Var(model.times_spectral, model.meas_lambdas)
            
            def rule_D_bar(model, t, l):
                if hasattr(model, 'huplc_absorbing') and hasattr(model, 'solid_spec_arg1'):
                    return model.D_bar[t, l] == sum(
                        getattr(model, self.component_var)[t, k] * model.S[l, k] for k in self.component_set if k not in model.solid_spec_arg1)
                else:
                    return model.D_bar[t, l] == sum(getattr(model, self.component_var)[t, k] * model.S[l, k] for k in self.component_set)

            model.D_bar_constraint = Constraint(model.times_spectral,
                                                model.meas_lambdas,
                                                rule=rule_D_bar)
        
        
        #For addition of huplc data and matching liquid and solid species (CS):
        def rule_Dhat_bar(model, t, l):
            list_huplcabs = [k for k in model.huplc_absorbing.value]
            return model.Dhat_bar[t, l] == (model.Z[t, l] + model.solidvol[t, l]) / (
                sum(model.Z[t, j] + model.solidvol[t, j] for j in list_huplcabs))

        def rule_objective(m):
            
            terms = {}
            obj_weight = {}
            
            terms['D_bar'] = self._get_objective_expr(m, with_d_vars, list_components, sigma_sq)
            obj_weight['D_bar'] = weights[0]

            terms['model_fit'] = 0
            obj_weight['model_fit'] = 1
            
            for t in m.times_spectral:
                terms['model_fit'] += sum((model.C[t, k] - model.Z[t, k]) ** 2 / sigma_sq[k] for k in list_components)
                
            terms['L2_penalty'] = 0
            obj_weight['L2_penalty'] = 1
            # L2 penalty term to objective penalizing values that deviate from values defined in ppenalty_dict:
            if penaltyparam==True:
                if ppenalty_weights is None:
                    terms['L2_penalty'] = 0.0
                    for k in model.P.keys():
                        if k in ppenalty_dict.keys():
                            terms['L2_penalty'] += (model.P[k] - ppenalty_dict[k]) ** 2
                else:
                    if len(ppenalty_dict)!=len(ppenalty_weights):
                        raise RuntimeError(
                            'For every penalty term a weight must be defined.')
                    if ppenalty_dict.keys()!=ppenalty_weights.keys():
                        raise RuntimeError(
                            'Check the parameter names in ppenalty_weights and ppenalty_dict again. They must match.')
                    else:
                        for k in model.P.keys():
                            if k in ppenalty_dict.keys():
                                terms['L2_penalty'] += ppenalty_weights[k] * (model.P[k] - ppenalty_dict[k]) ** 2

            terms['huplc'] = 0
            obj_weight['huplc'] = 1
            terms['constraint_penalty'] = 0
            obj_weight['constraint_penalty'] = 1
            
            # for new huplc structure (CS):
            if hasattr(model, 'huplc_absorbing'):
                terms['huplc'] = self._huplc_obj_term(model, sigma_sq)
                
                # This might break - I don't have anything to compare it too
                if penaltyparamcon == True: #added for optional penalty term related to constraint CS
                    rho=1e-1
                    sumpen=0.0
                    for t in model.alltime:
                        sumpen = sumpen + m.Y[t,'npen']
                    terms['constraint_penalty'] = rho*sumpen

            expr = 0
            print('expr =')
            for k in terms.keys():
                print(f' + {obj_weight[k]} * {k}')
                expr += terms[k] * obj_weight[k]

            return expr

        # Estimation without model variance and only device variance
        def rule_objective_device_only(model):
            
            terms = {}
            obj_weight = {}
            
            terms['D_bar'] = 0
            obj_weight['D_bar'] = 1
            terms['huplc'] = 0
            obj_weight['huplc'] = 1
            
            if hasattr(model, 'huplc_absorbing'):
                component_set = model._abs_components
            else:
                component_set = list_components
            
            terms['D_bar'] = self._get_objective_expr(model, with_d_vars, component_set, sigma_sq, device=True)
            
            if hasattr(model, 'huplc_absorbing'):
                terms['huplc'] = self._huplc_obj_term(model, sigma_sq)
                      
            expr = 0
            print('expr =')
            for k in terms.keys():
                print(f' + {obj_weight[k]} * {k}')
                expr += terms[k] * obj_weight[k]

            return expr

        if self.model_variance == True:
            model.objective = Objective(rule=rule_objective)
        else:
            model.objective = Objective(rule=rule_objective_device_only)

        custom_weight = 1
        if hasattr(model, 'custom_obj'):
            model.objective.expr += custom_weight*(model.custom_obj)

        if warmstart==True:
            if hasattr(model,'dual') and hasattr(model,'ipopt_zL_out') and hasattr(model,'ipopt_zU_out') and hasattr(model,'ipopt_zL_in') and hasattr(model,'ipopt_zU_in'):
                self.update_warm_start(model)
            else:
                self.add_warm_start_suffixes(model, use_k_aug=False)

        if self.solver in ['k_aug', 'ipopt_sens']:

            if self.solver == 'ipopt_sens':
                hessian = self._covariance_ipopt_sens(model, optimizer, tee, all_sigma_specified)
                
            elif self.solver == 'k_aug':
                hessian = self._covariance_k_aug(model, optimizer, tee, all_sigma_specified)
                
            if self.model_variance:
                hessian_out = self._compute_covariance(hessian, sigma_sq)
                
            print(hessian_out)
                
            self.cov = pd.DataFrame(hessian_out, index=self.param_names, columns=self.param_names)   
            cov_mat = self.cov.values
        
        else:
            solver_results = optimizer.solve(model, tee=tee) 
           
        if with_d_vars:
            model.del_component('D_bar')
            model.del_component('D_bar_constraint')
        
        obj_val = model.objective.expr()
        model.del_component('objective')
        
        return obj_val, cov_mat
        
    
    def _solve_model_given_c(self, sigma_sq, optimizer, **kwds):
        """Solves estimation based on concentration data. (known variances)

        This method is not intended to be used by users directly

        :param dict sigma_sq: variances
        :param SolverFactory optimizer: Pyomo Solver factory object

        :Keyword Args:

            - tee (bool,optional): flag to tell the optimizer whether to stream output
              to the terminal or not

        :return: None

        """
        tee = kwds.pop('tee', False)
        
        if self._huplc_given:
            weights = kwds.pop('weights', [0.0, 1.0, 1.0])
        else:
            weights = kwds.pop('weights', [0.0, 1.0])
       
        covariance = kwds.pop('covariance', False)
        warmstart = kwds.pop('warmstart', False)
        penaltyparamcon = kwds.pop('penaltyparamcon', False) #added for optional penalty term related to constraint CS
        species_list = kwds.pop('subset_components', None)
        cov_mat = None

        list_components = self._get_list_components(species_list)
        model = self.model

        if not self._concentration_given: # and not self._custom_data_given:
            raise NotImplementedError(
                "Parameter Estimation from concentration data requires concentration data model.C[ti,cj]")

        all_sigma_specified = True

        keys = sigma_sq.keys()
        
        # HUPLC shows up here too
        for k in list_components:
            if hasattr(self, 'huplc_absorbing') and k not in keys:
                for ki in self.solid_spec_args1:
                    for key in keys:
                        if key == ki:
                            sigma_sq[ki] = sigma_sq[key]

            elif hasattr(self, 'huplc_absorbing') == False and k not in keys:
                all_sigma_specified = False
                sigma_sq[k] = max(sigma_sq.values())

        def rule_objective(model):
            obj=0
            if penaltyparamcon == True:
                rho = 100
                sumpen = 0.0
                obj += conc_objective(model, variance=sigma_sq)    
                obj += comp_objective(model)
                
                # Is this correct?
                for t in model.allmeas_times:
                    sumpen += model.Y[t, 'npen']
                fifth_term = rho * sumpen
                obj += fifth_term
            else:
                obj += conc_objective(model, variance=sigma_sq)
                obj += comp_objective(model)
            return obj

        model.objective = Objective(rule=rule_objective)

        
        # Add custom objective
        if hasattr(model, 'custom_obj'):
            model.objective.expr += model.custom_obj

        if warmstart==True:
            if hasattr(model,'dual') and hasattr(model,'ipopt_zL_out') and hasattr(model,'ipopt_zU_out') and hasattr(model,'ipopt_zL_in') and hasattr(model,'ipopt_zU_in'):
                self.update_warm_start(model)
            else:
                self.add_warm_start_suffixes(model)


        self.cov = None
        if self.solver in ['k_aug', 'ipopt_sens']:
            
            if self.solver == 'ipopt_sens':
                hessian = self._covariance_ipopt_sens(model, optimizer, tee, all_sigma_specified)
                
            elif self.solver == 'k_aug':
                hessian = self._covariance_k_aug(model, optimizer, tee, all_sigma_specified, labels=True)
                
            self.cov = pd.DataFrame(hessian, index=self.param_names, columns=self.param_names)   
               
        else:
            solver_results = optimizer.solve(model, tee=tee, symbolic_solver_labels=True)
            self._termination_problems(solver_results, optimizer)
            
        obj_val = model.objective.expr()
        model.del_component('objective')
        
        return obj_val, cov_mat
    
    def _covariance_ipopt_sens(self, model, optimizer, tee, all_sigma_specified):
        """Generalize the covariance optimization with IPOPT Sens

        :param ConcreteModel model: The Pyomo model used in parameter fitting
        :param SolverFactory optimizer: The SolverFactory currently being used
        :param bool tee: Display option
        :param dict all_sigma_specified: The provided variances

        :return hessian: The covariance matrix
        :rtype: numpy.ndarray

        """
        if self.model_variance == False:
            print("WARNING: FOR PROBLEMS WITH NO MODEL VARIANCE it is advised to use k_aug!!!")
        self._tmpfile = "ipopt_hess"
        
        solver_results = optimizer.solve(model, 
                                         tee=tee,
                                         logfile=self._tmpfile,
                                         report_timing=True)
        
        print("Done solving building reduce hessian")
        output_string = ''
        with open(self._tmpfile, 'r') as f:
            output_string = f.read()
        if os.path.exists(self._tmpfile):
            os.remove(self._tmpfile)

        ipopt_output, hessian_output = split_sipopt_string(output_string)
        
        if not all_sigma_specified:
            raise RuntimeError(
                'All variances must be specified to determine covariance matrix.\n Please pass variance dictionary to run_opt')

        n_vars = len(self._idx_to_variable)
        print(n_vars)
        
        hessian = read_reduce_hessian(hessian_output, n_vars)
        
        print(f'THE SIZE: {hessian.shape}')
        
        import pandas as pd
        
        self.hessian = pd.DataFrame(hessian)
        
        print(self.hessian)
        
        return hessian
    
    def _covariance_k_aug(self, model, optimizer, tee, all_sigma_specified, labels=False):
        """Generalize the covariance optimization with IPOPT Sens

        :param ConcreteModel model: The Pyomo model used in parameter fitting
        :param SolverFactory optimizer: The SolverFactory currently being used
        :param bool tee: Display option
        :param dict all_sigma_specified: The provided variances
        :param bool labels: Display options

        :return hessian: The covariance matrix
        :rtype: numpy.ndarray

        """
        self.add_warm_start_suffixes(model, use_k_aug=True)   
    
        self._tmpfile = "k_aug_hess"
        ip = SolverFactory('ipopt')
        
        solver_results = ip.solve(model,
                                  tee=tee,
                                  logfile=self._tmpfile,
                                  report_timing=True,
                                  symbolic_solver_labels=True,
                                  keepfiles=True
                                  )
    
        if labels:
            self._termination_problems(solver_results, optimizer)
        
        k_aug = SolverFactory('k_aug')
        self.update_warm_start(model)
        k_aug.options["print_kkt"] = ""
        k_aug.solve(model, tee=True)
        
        inverse_reduced_hessian = self.calculate_inverse_Hr(self._tmpfile, self._idx_to_variable, self.param_names_full)

        return inverse_reduced_hessian
    
    
    @staticmethod
    def calculate_inverse_Hr(tmp_file, variable_index, param_list):
            
        #%%
        # param_names = []
        # tmp_file = r1.p_estimator._tmpfile
        # variable_index = r1.p_estimator._idx_to_variable
        
        # param_names = [p for p in getattr(r1.p_estimator.model, 'P')]
        # param_list = [f'P[{p}]' for p in getattr(r1.p_estimator.model, 'P')]
        # if hasattr(r1.p_estimator.model, 'Pinit'):
        #     param_names += [p for p in getattr(r1.p_estimator.model, 'Pinit')]
        #     param_list += [f'init_conditions[{p}]' for p in getattr(r1.p_estimator.model, 'Pinit')]
        
        
        from pathlib import Path
        import pandas as pd
        import numpy as np
        from scipy.sparse import coo_matrix, csc_matrix, triu
        from scipy.sparse.linalg import spsolve
        from kipet.calculation_tools.reduced_hessian import SparseRowIndexer, delete_from_csr
        
        kaug_files = Path('GJH')

        with open(tmp_file, 'r') as f:
            output_string = f.read()

        stub = output_string.split('\n')[0].split(',')[1][2:-4]

        var_index = pd.read_csv(Path(stub + '.col'), sep=';', header=None)  # dummy sep
        con_index = pd.read_csv(Path(stub + '.row'), sep=';', header=None)  # dummy sep
        var_index_names = [var_name for var_name in var_index[0]]
        con_index_names = [con_name for con_name in con_index[0].iloc[:-1]]
        
        hess_file = kaug_files.joinpath('H_print.txt')
        hess = pd.read_csv(hess_file, delim_whitespace=True, header=None, skipinitialspace=True)
        hess.columns = ['irow', 'jcol', 'vals']
        hess.irow -= 1
        hess.jcol -= 1

        jac_file = kaug_files.joinpath('A_print.txt')
        jac = pd.read_csv(jac_file, delim_whitespace=True, header=None, skipinitialspace=True)
        jac.columns = ['irow', 'jcol', 'vals']
        jac.irow -= 1
        jac.jcol -= 1

        n = len(var_index_names)
        m = len(con_index_names)
        
        J = coo_matrix((jac.vals, (jac.jcol, jac.irow)), shape=(m, n))
        J_c = J.tocsc()
        Hess_coo = coo_matrix((hess.vals, (hess.irow, hess.jcol)), shape=(n, n))
        H = Hess_coo + triu(Hess_coo, 1).T
        
        # H_df = pd.DataFrame(H.todense(), columns=var_index_names, index=var_index_names)
     
        # print(var_index_names)
        # print(n)
        # print(H_df)
     
        col_ind = [var_index_names.index(v.getname()) for v in variable_index.values()]
        # col_dict = {v.getname(): var_index_names.index(v.getname()) for v in variable_index.values()}
        
        col_ind_P = [var_index_names.index(name) for name in param_list]
        col_ind_P_in_Hr = [col_ind.index(p) for p in col_ind_P]
        
        # col_dict = {v.getname(): var_index_names.index(v.getname()) for v in param_list}
        
        row_indexer = SparseRowIndexer(J_c.T)
        J_f = row_indexer[col_ind].T
        J_l = delete_from_csr(J_c.tocsr(), col_indices=col_ind)

        n_free = n - J_f.shape[0]
        
        X = spsolve(J_l.tocsc(), -J_f.tocsc())

        col_ind_left = list(set(range(n)).difference(set(col_ind)))
        col_ind_left.sort()

        Z = np.zeros([n, n_free])
        Z[col_ind, :] = np.eye(n_free)

        if isinstance(X, csc_matrix):
            Z[col_ind_left, :] = X.todense()
        else:
            Z[col_ind_left, :] = X.reshape(-1, 1)

        Z_mat = coo_matrix(np.mat(Z)).tocsr()
        Z_mat_T = coo_matrix(np.mat(Z).T).tocsr()
        Hess = H.tocsr()
        reduced_hessian = Z_mat_T * Hess * Z_mat
        inv_H_r = np.linalg.inv(reduced_hessian.todense())
        
        H_use = inv_H_r[col_ind_P_in_Hr, :]
    
        #%%
    
        return H_use
    
    def _termination_problems(self, solver_results, optimizer):
        """Checks the termination conditions and will try once again if it fails

        :param ResultsObject solver_results: The results from the parameter fittings
        :param SolverFactory optimizer: The solver factory being used

        :return: None

        """
        self.termination_condition = solver_results.solver.termination_condition
        if self.termination_condition != TerminationCondition.optimal:
            print("WARNING: The solution of the iteration was unsuccessful. The problem is solved with additional solver options.")
            optimizer.options["OF_start_with_resto"] = 'yes'
            solver_results = optimizer.solve(self.model, tee=False, symbolic_solver_labels=True)
            self.termination_condition = solver_results.solver.termination_condition
            if self.termination_condition != TerminationCondition.optimal:
                print(
                    "WARNING: The solution of the iteration was unsuccessful. The problem is solved with additional solver options.")
                optimizer.options["OF_start_with_resto"] = 'no'
                # optimizer.options["OF_bound_push"] = 1E-02
                optimizer.options["OF_bound_relax_factor"] = 1E-05
                solver_results = optimizer.solve(self.model, tee=False, symbolic_solver_labels=True)
                self.termination_condition = solver_results.solver.termination_condition
                # options["OF_bound_relax_factor"] = 1E-08
                if self.termination_condition != TerminationCondition.optimal:
                        print("The current iteration was unsuccessful.")
                        
        return None

     #For addition of huplc data and matching liquid and solid species (CS):
        
    def _huplc_obj_term(self, m, sigma_sq):
        """Adds the HUPLC term to the objective

        :param ConcreteModel m: The model used in parameter fitting
        :param dict sigma_sq: The dict of variances

        :return expressions third_term: The HUPLC objective expression

        """
        #print(m, sigma_sq)
        
        
        def rule_Dhat_bar(m, t, l):
            list_huplcabs = [k for k in m.huplc_absorbing.value]
            return m.Dhat_bar[t, l] == (m.Z[t, l] + m.solidvol[t, l]) / (
                sum(m.Z[t, j] + m.solidvol[t, j] for j in list_huplcabs))

        third_term = 0.0
        
        # Arrange the HUPLC device variance
        if not 'device-huplc' in sigma_sq.keys():
            sigma_sq['device-huplc'] = 1.0
            
        if hasattr(m, 'solid_spec_arg1') and hasattr(m, 'solid_spec_arg2'):
            solidvol_dict = dict()
            m.add_component('cons_solidvol', ConstraintList())
            new_consolidvol = getattr(m, 'cons_solidvol')
            m.add_component('solidvol', Var(m.huplctime, m.huplc_absorbing.value, initialize=solidvol_dict))

            for k in m.solid_spec_arg1:
                for j in m.algebraics:
                    for time in m.huplctime:
                        if j == k:
                            for l in m.huplc_absorbing.value:
                                strsolidspec = "\'" + str(k) + "\'" + ', ' + "\'" + str(
                                    l) + "\'"  # pair of absorbing solid and liquid
                                if l in m.solid_spec_arg2 and strsolidspec in str(
                                        m.solid_spec.keys()):  #check whether pair of solid and liquid in keys and whether liquid in huplcabs species
                                    valY = value(m.Y[time, k]) / value(m.vol)
                                    if valY <= 0:
                                        new_consolidvol.add(m.solidvol[time, l] == 0.0)
                                    else:
                                        new_consolidvol.add(m.solidvol[time, l] == m.Y[time, k] / m.vol)
                                else:
                                    new_consolidvol.add(m.solidvol[time, l] == 0.0)
                for jk in self._get_list_components(species_list):
                    for time in m.huplctime:
                        if jk == k:
                            for l in m.huplc_absorbing.value:
                                strsolidspec = "\'" + str(k) + "\'" + ', ' + "\'" + str(
                                    l) + "\'"  # pair of absorbing solid and liquid
                                if l in m.solid_spec_arg2 and strsolidspec in str(
                                        m.solid_spec.keys()):  #check whether pair of solid and liquid in keys and whether liquid in huplcabs species
                                    valZ = value(m.Z[time, k]) / value(m.vol)
                                    if valZ <= 0:
                                        new_consolidvol.add(m.solidvol[time, l] == 0.0)
                                    else:
                                        new_consolidvol.add(m.solidvol[time, l] == m.Z[time, k] / m.vol)
                                else:
                                    new_consolidvol.add(m.solidvol[time, l] == 0.0)

            m.Dhat_bar = Var(m.huplcmeas_times,
                             m.huplc_absorbing)

            m.Dhat_bar_constraint = Constraint(m.huplcmeas_times,
                                               m.huplc_absorbing,
                                               rule=rule_Dhat_bar)

            for t in m.huplcmeas_times:
                list_huplcabs = [k for k in m.huplc_absorbing.value]
                for k in list_huplcabs:
                    third_term += (m.Dhat[t, k] - m.Dhat_bar[t, k]) ** 2 / sigma_sq['device-huplc']

        return third_term

    def _define_reduce_hess_order(self):
        """
        This sets up the suffixes of the reduced hessian

        :return: None

        """
        self.model.red_hessian = Suffix(direction=Suffix.IMPORT_EXPORT)
        count_vars = 1

        if self._spectra_given:
            if self.model_variance:
                count_vars = self._set_up_reduced_hessian(self.model, self.model.times_spectral, self.component_set, self.component_var, count_vars)
                count_vars = self._set_up_reduced_hessian(self.model, self.model.meas_lambdas, self.component_set, 'S', count_vars)
                
        for v in self.model.P.values():
            if v.is_fixed():
                print(v, end='\t')
                print("is fixed")
                continue
            self._idx_to_variable[count_vars] = v
            self.model.red_hessian[v] = count_vars
            count_vars += 1
            
        if hasattr(self.model, 'Pinit'):
            for k, v in self.model.Pinit.items():
                v = self.model.init_conditions[k]
                self._idx_to_variable[count_vars] = v
                self.model.red_hessian[v] = count_vars
                count_vars += 1
               
        return None
        
    def _compute_covariance(self, H, variances):
        """Computes the covariance for post calculation anaylsis

        :param numpy.ndarray hessian: The Hessian matrix
        :param dict variances: Component variances

        :return: The parameter covariances
        
        """
        B = self._compute_B_matrix(variances)
        Vd = self._compute_Vd_matrix(variances)
        
        print(f'B: {B.shape}')
        print(f'H: {H.shape}')
        print(f'Vd: {Vd.shape}')
        
        R = B.T @ H.T
        A = Vd @ R
        L = H @ B
        V_theta = (A.T @ L.T).T

        covariances_p = V_theta
        
        print('V_theta')
        print(V_theta)

        return covariances_p

    def _compute_B_matrix(self, variances, **kwds):
        """Builds B matrix for calculation of covariances

        This method is not intended to be used by users directly

        :param dict variances: variances

        :return: None

        """
        nt = len(self.model.times_spectral)
        time_set = self.model.times_spectral
        
        conc_data_var = 'C'
        nw = len(self.model.meas_lambdas)
        nparams = self._get_nparams(self.model)
       
        if hasattr(self, '_abs_components'):
            n_val = self._nabs_components
            component_set = self._abs_componets
        else:
            n_val = self._n_actual
            component_set = self._sublist_components
    
        variance = variances['device']
        ntheta = n_val * (nw + nt) + nparams
        B_matrix = np.zeros((ntheta, nw * nt))

        for i, t in enumerate(time_set):
            for j, l in enumerate(self.model.meas_lambdas):
                for k, c in enumerate(component_set):
                    r_idx1 = i * n_val + k
                    r_idx2 = j * n_val + k + n_val * nt
                    c_idx = i * nw + j
                    B_matrix[r_idx1, c_idx] = -2 * self.model.S[l, c].value / variance
                    B_matrix[r_idx2, c_idx] = -2 * getattr(self.model, conc_data_var)[t, c].value / variance
                    
        return B_matrix

    def _compute_Vd_matrix(self, variances, **kwds):
        """Builds d covariance matrix

        This method is not intended to be used by users directly

        :param dict variances: variances

        :return: None

        """
        nt = len(self.model.times_spectral)
        nw = len(self.model.meas_lambdas)
        row = []
        col = []
        data = []
        nd = nt * nw
        v_device = variances['device']

        s_array = np.zeros(nw * self.n_val)
        v_array = np.zeros(self.n_val)
        
        for k, c in enumerate(self.component_set):
            v_array[k] = variances[c]

        for j, l in enumerate(self.model.meas_lambdas):
            for k, c in enumerate(self.component_set):
                s_array[j * self.n_val + k] = self.model.S[l, c].value

        for i in range(nt):
            for j in range(nw):
                val = sum(v_array[k] * s_array[j * self.n_val + k] ** 2 for k in range(self.n_val)) + v_device
                row.append(i * nw + j)
                col.append(i * nw + j)
                data.append(val)

                for p in range(nw):
                    if j != p:
                        val = sum(v_array[k] * s_array[j * self.n_val + k] * s_array[p * self.n_val + k] for k in range(self.n_val))
                        row.append(i * nw + j)
                        col.append(i * nw + p)
                        data.append(val)

        Vd_matrix = coo_matrix((data, (row, col)), shape=(nd, nd)).tocsr()
        
        return Vd_matrix

    def run_param_est_with_subset_lambdas(self, builder_clone, end_time, subset, nfe, ncp, sigmas, solver='ipopt'):
        """ Performs the parameter estimation with a specific subset of wavelengths.
            At the moment, this is performed as a totally new Pyomo model, based on the
            original estimation. Initialization strategies for this will be needed.

        :param TemplateBuilder builder_clone: Template builder class of complete model without the data added yet
        :param float end_time: the end time for the data and simulation
        :param list subset: list of selected wavelengths
        :param int nfe: number of finite elements
        :param int ncp: number of collocation points
        :param dict sigmas: dictionary containing the variances, as used in the ParameterEstimator class

        :return ResultsObject results: The solved pyomo model results

        """
        if not isinstance(subset, (list, dict)):
            raise RuntimeError("subset must be of type list or dict!")

        if isinstance(subset, dict):
            lists1 = sorted(subset.items())
            x1, y1 = zip(*lists1)
            subset = list(x1)
        
        # This is the filter for creating the new data subset
        old_D = convert(self.model.D)
        new_D = old_D.loc[:, subset] 
        
        
        print(end_time, new_D)
        # Now that we have a new DataFrame, we need to build the entire problem from this
        # An entire new ParameterEstimation problem should be set up, on the outside of
        # this function and class structure, from the model already developed by the user.
        new_template = construct_model_from_reduced_set(builder_clone, end_time, new_D)
        # need to put in an optional running of the variance estimator for the new
        # parameter estiamtion run, or just use the previous full model run to initialize...

        results, lof = run_param_est(new_template, nfe, ncp, sigmas, solver=solver)

        return results

    def run_lof_analysis(self, builder_before_data, end_time, correlations, lof_full_model, nfe, ncp, sigmas,
                         step_size=0.2, search_range=(0, 1)):
        """ Runs the lack of fit minimization problem used in the Michael's Reaction paper
        from Chen et al. (submitted). To use this function, the full parameter estimation
        problem should be solved first and the correlations for wavelngths from this optimization
        need to be supplied to the function as an option.


        :param TemplateBuilder builder_before_data: Template builder class of complete model without the data added yet
        :param int end_time: the end time for the data and simulation
        :param dict correlations: dictionary containing the wavelengths and their correlations to the concentration profiles
        :param int lof_full_model: the value of the lack of fit of the full model (with all wavelengths)
        :param int nfe: number of finite elements
        :param int ncp: number of collocation points
        :param dict sigmas: dictionary containing the variances, as used in the ParameterEstimator class
        :param float step_size: The spacing used in correlation thresholds
        :param tuple search_range: correlation bounds within to search

        :return: None

        """
        if not isinstance(step_size, float):
            raise RuntimeError("step_size must be a float between 0 and 1")
        elif step_size >= 1 or step_size <= 0:
            return RuntimeError("step_size must be a float between 0 and 1")

        if not isinstance(search_range, tuple):
            raise RuntimeError("search range must be a tuple")
        elif search_range[0] < 0 or search_range[0] > 1 and not (
                isinstance(search_range, float) or isinstance(search_range, int)):
            raise RuntimeError("search range lower value must be between 0 and 1 and must be type float")
        elif search_range[1] < 0 or search_range[1] > 1 and not (
                isinstance(search_range, float) or isinstance(search_range, int)):
            raise RuntimeError("search range upper value must be between 0 and 1 and must be type float")
        elif search_range[1] <= search_range[0]:
            raise RuntimeError("search_range[1] must be bigger than search_range[0]!")
        # firstly we will run the initial search from at increments of 20 % for the correlations
        # we already have lof(0) so we want 10,30,50,70, 90.
        
        count = 0
        filt = 0.0
        initial_solutions = list()
        initial_solutions.append((0, lof_full_model))
        while filt < search_range[1]:
            filt += step_size
            if filt > search_range[1]:
                break
            elif filt == 1:
                break
            new_subs = wavelength_subset_selection(correlations=correlations, n=filt)
            lists1 = sorted(new_subs.items())
            x1, y1 = zip(*lists1)
            x = list(x1)

            old_D = convert(self.model.D)
            new_D = old_D.loc[:, new_subs]

            # opt_model, nfe, ncp = construct_model_from_reduced_set(builder_before_data, end_time, new_D)
            # Now that we have a new DataFrame, we need to build the entire problem from this
            # An entire new ParameterEstimation problem should be set up, on the outside of
            # this function and class structure, from the model already developed by the user.
            new_template = construct_model_from_reduced_set(builder_before_data, end_time, new_D)
            # need to put in an optional running of the variance estimator for the new
            # parameter estimation run, or just use the previous full model run to initialize...
            results, lof = run_param_est(new_template, nfe, ncp, sigmas)
            initial_solutions.append((filt, lof))

            count += 1

        count = 0
        for x in initial_solutions:
            print(f'When wavelengths of less than {x[0]:0.3f} correlation are removed')
            print(f'The lack of fit is {x[1]:0.6f} %')

    # =============================================================================
    # --------------------------- DIAGNOSTIC TOOLS ------------------------
    # =============================================================================

    def lack_of_fit(self):
        """ Runs basic post-processing lack of fit analysis

        :return float lack of fit: percentage lack of fit

        """
        
        if self._spectra_given:
        
            sum_e = 0
            sum_d = 0
            C = np.zeros((len(self.model.times_spectral), self.n_val))
            S = np.zeros((len(self.model.meas_lambdas), self.n_val))
            
            for c_count, c in enumerate(self.component_set):
                for t_count, t in enumerate(self.model.times_spectral):
                    C[t_count, c_count] = getattr(self.model, self.component_var)[t, c].value
    
            for c_count, c in enumerate(self.component_set):
                for l_count, l in enumerate(self.model.meas_lambdas):
                    S[l_count, c_count] = self.model.S[l, c].value
                 
            D_model = C.dot(S.T)
            
            for t_count, t in enumerate(self.model.times_spectral):
                for l_count, l in enumerate(self.model.meas_lambdas):
                    sum_e += (D_model[t_count, l_count] - self.model.D[t, l]) ** 2
                    sum_d += (self.model.D[t, l]) ** 2
      
            lof = np.sqrt(sum_e/sum_d)*100
            
        elif self._concentration_given:
            
            sum_e = 0
            sum_d = 0
           
            for index, values in self.model.Cm.items():
                sum_e += (self.model.Z[index].value - self.model.Cm[index].value) ** 2
                sum_d += (self.model.Cm[index].value) ** 2

            lof = np.sqrt(sum_e/sum_d)*100
            
        #print(f'The lack of fit is {lof:0.2f}%')
        return lof

    def wavelength_correlation(self):
        """ determines the degree of correlation between the individual wavelengths and
        the and the concentrations.


        :return dict: dictionary of correlations with wavelength

        """
        nt = len(self.model.allmeas_times)

        cov_d_l = dict()
        for c in self._sublist_components:
            for l in self.model.meas_lambdas:
                mean_d = (sum(self.model.D[t, l] for t in self.model.times_spectral) / nt)
                mean_c = (sum(self.model.C[t, c].value for t in self.model.times_spectral) / nt)
                cov_d_l[l, c] = 0
                for t in self.model.times_spectral:
                    cov_d_l[l, c] += (self.model.D[t, l] - mean_d) * (self.model.C[t, c].value - mean_c)

                cov_d_l[l, c] = cov_d_l[l, c] / (nt - 1)

        # calculating the standard devs for dl and ck over time
        s_dl = dict()

        for l in self.model.meas_lambdas:
            s_dl[l] = 0
            mean_d = (sum(self.model.D[t, l] for t in self.model.times_spectral) / nt)
            error = 0
            for t in self.model.times_spectral:
                error += (self.model.D[t, l] - mean_d) ** 2
            s_dl[l] = (error / (nt - 1)) ** 0.5

        s_ck = dict()

        for c in self._sublist_components:
            s_ck[c] = 0
            mean_c = (sum(self.model.C[t, c].value for t in self.model.times_spectral) / nt)
            error = 0
            for t in self.model.times_spectral:
                error += (self.model.C[t, c].value - mean_c) ** 2
            s_ck[c] = (error / (nt - 1)) ** 0.5

        cor_lc = dict()

        for c in self._sublist_components:
            for l in self.model.meas_lambdas:
                cor_lc[l, c] = cov_d_l[l, c] / (s_ck[c] * s_dl[l])

        cor_l = dict()
        for l in self.model.meas_lambdas:
            cor_l[l] = max(cor_lc[l, c] for c in self._sublist_components)

        return cor_l

    def lack_of_fit_huplc(self):
        """ Runs basic post-processing lack of fit analysis

        :return float lack of fit: percentage lack of fit

        """
        nc = len(self.model.huplc_absorbing)
        sum_e = 0
        sum_d = 0
        D_model = np.zeros((len(self.model.huplcmeas_times), nc))
        
        for t_count, t in enumerate(self.model.huplcmeas_times):
            for l_count, l in enumerate(self._list_huplcabs):
                
                if hasattr(self.model, 'solidvol'):
                    D_model[t_count, l_count] = (self.model.Z[t, l].value + self.model.solidvol[t, l].value) / (
                        sum(self.model.Z[t, j].value + self.model.solidvol[t, j].value for j in self._list_huplcabs))
                else:
                    D_model[t_count, l_count] = (self.model.Z[t, l].value) / (
                        sum(self.model.Z[t, j].value for j in self._list_huplcabs))

                sum_e += (D_model[t_count, l_count] - self.model.Dhat[t, l].value) ** 2
                sum_d += (self.model.Dhat[t, l].value) ** 2

        lof = np.sqrt((sum_e/sum_d))*100

        print(f"The lack of fit for the huplc data is {lof:0.2f}%")
        return lof
    
    def g_handling_status_messages(self):
        """Determines the unwanted contribution type and informs the user of this

        :return: None

        """
        if self.G_contribution == 'unwanted_G':
            print("\nType of unwanted contributions not set, so assumed that it is time-variant.\n")
            self.G_contribution = 'time_variant_G'
        elif self.G_contribution == 'time_variant_G':
            print("\nTime-variant unwanted contribution is involved.\n")
        elif self.G_contribution == 'time_invariant_G_decompose':
            print("\nTime-invariant unwanted contribution is involved and G can be decomposed.\n")
        elif self.G_contribution == 'time_invariant_G_no_decompose':
            print("\nTime-invariant unwanted contribution is involved but G cannot be decomposed.\n")
        return None
     
    def decompose_G_test(self, St, Z_in):
        """Check whether or not G can be decomposed

        :param dict St: Reaction coefficient matrix
        :param dict Z_in: Dosing points

        :return: None

        """
        if St == dict() and Z_in == dict():
            raise RuntimeError('Because time-invariant unwanted contribution is chosen, please provide information of St or Z_in to build omega matrix.')
        
        omega_list = [St[i] for i in St.keys()]
        omega_list += [Z_in[i] for i in Z_in.keys()]
        omega_sub = np.array(omega_list)
        rank = np.linalg.matrix_rank(omega_sub)
        cols = omega_sub.shape[1]
        rko = cols - rank
        
        if rko > 0:
            self.time_invariant_G_decompose = True
            self.G_contribution = 'time_invariant_G_decompose'
        else:
            self.time_invariant_G_no_decompose = True
            self.G_contribution = 'time_invariant_G_no_decompose'
        return None

def wavelength_subset_selection(correlations=None, n=None):
    """ identifies the subset of wavelengths that needs to be chosen, based
    on the minimum correlation value set by the user (or from the automated
    lack of fit minimization procedure)

    :param dict correlations: dictionary obtained from the wavelength_correlation  function, containing every
       wavelength from the original set and their correlations to the concentration profile.
    :param int n: a value between 0 - 1 that slects the minimum amount correlation between the wavelength and the
       concentrations.

    :return: A dictionary of correlations with wavelength
    :rtype: dict

    """
    if not isinstance(correlations, dict):
        raise RuntimeError("correlations must be of type dict()! Use wavelength_correlation function first!")

    # should check whether the dictionary contains all wavelengths or not
    if not isinstance(n, float):
        raise RuntimeError("n must be of type int!")
    elif n > 1 or n < 0:
        raise RuntimeError("n must be a number between 0 and 1")

    subset_dict = dict()
    for l in correlations.keys():
        if correlations[l] >= n:
            subset_dict[l] = correlations[l]
    return subset_dict


# =============================================================================
# ----------- PARAMETER ESTIMATION WITH WAVELENGTH SELECTION ------------------
# =============================================================================

def construct_model_from_reduced_set(builder_clone, end_time, D):
    """ constructs the new pyomo model based on the selected wavelengths.

    :param TemplateBuilder builder_clone: Template builder class of complete model without the data added yet
    :param float end_time: The end time for the data and simulation
    :param pandas.DataFrame D: The new, reduced dataset with only the selected wavelengths.

    :return TemplateBuilder opt_mode: new Pyomo model from TemplateBuilder, ready for parameter estimation

    """
    import pandas as pd
    from kipet.model_tools.template_builder import TemplateBuilder
    if not isinstance(builder_clone, TemplateBuilder):
        raise RuntimeError('builder_clone needs to be of type TemplateBuilder')

    if not isinstance(D, pd.DataFrame):
        raise RuntimeError('Spectral data format not supported. Try pandas.DataFrame')

    builder_clone._spectral_data = D
    opt_model = builder_clone.create_pyomo_model(0.0, end_time)

    return opt_model


def run_param_est(opt_model, nfe, ncp, sigmas, solver='ipopt'):
    """ Runs the parameter estimator for the selected subset

    :param ConcreteModel opt_model: The model that we wish to run the
    :param int nfe: The number of finite elements
    :param int ncp: The number of collocation points
    :param dict sigmas: A dictionary containing the variances, as used in the ParameterEstimator class

    :return results_pyomo: Parameter Estimation results
    :return lof: lack of fit results

    """
    p_estimator = ParameterEstimator(opt_model)
    p_estimator.apply_discretization('dae.collocation', nfe=nfe, ncp=ncp, scheme='LAGRANGE-RADAU')
    options = dict()

    

    # These may not always solve, so we need to come up with a decent initialization strategy here
    if solver == 'ipopt':
        results_pyomo = p_estimator.run_opt('ipopt',
                                            tee=False,
                                            solver_opts=options,
                                            variances=sigmas)
    else:
        results_pyomo = p_estimator.run_opt(solver,
                                            tee=False,
                                            solver_opts=options,
                                            variances=sigmas,
                                            covariance=True)
    
    lof = p_estimator.lack_of_fit()

    return results_pyomo, lof
