# Standard library imports
from operator import mod
from os import getcwd

# Third party imports
from pyomo.dae import ContinuousSet, DerivativeVar
from pyomo.environ import Constraint, ConstraintList, Param, TransformationFactory, value, Var
from pyomo.opt import ProblemFormat, SolverFactory, TerminationCondition

# KIPET library imports
from kipet.calculation_tools.interpolation import interpolate_trajectory
from kipet.model_tools.visitor_classes import ReplacementVisitor
from kipet.general_settings.variable_names import VariableNames
from kipet.model_tools.pyomo_model_tools import (change_continuous_set,
                                                  get_index_sets)
from kipet.general_settings.settings import solver_path

__author__ = 'David M Thierry, Kevin McBride'  #: April 2018 - May 2021


class FEInitialize(object):
    """This class implements the finite per finite element initialization for
    a pyomo model initialization. A march-forward simulation will be run and 
    the resulting data will be patched to the tgt_model.
    
    The current strategy is as follows:
    1. Create a copy of the undiscretized model.
    2. Change the corresponding time set bounds to (0,1).
    3. Discretize and create the new model with the parameter h_i.
    4. Deactivate initial conditions.
    5. Check for params and inputs.

    
    .. note::
        
        An input needs to be a variable(fixed) indexed over time. Otherwise 
        it would be a parameter.

    """

    def __init__(self,
                 model_orig,
                 src_mod,
                 init_con=None,
                 param_name=None,
                 param_values=None,
                 inputs_sub=None,
                 fixed_states=None,
                 ):
        """
        The `the paran name` might be a list of strings or a single string
          corresponding to the parameters of the model.
        The `param_values` dictionary needs to be declared with the following 
        syntax: `param_dict["P", "k0"] = 49.7796`
        
        Where the first key corresponds to one of the parameter names, and the
        second to the corresponding index (if any).
        
        A similar structure is expected for the initial conditions and inputs.

        The `inputs` and `input_sub` parameters are in place depending of 
        whether there is a single index input or a multiple index input.

        Note that if the user does not provide correct information to 
        fe_factory; an exception will be thrown because of the n_var and m_eqn
        check for simulation.

        Once the constructor is called, one can initialize the model with the 
        following sintax: `self.load_initial_conditions(init_cond=ics_dict)`

        Finally, to run the initialization and automatic data patching to tgt
        model use: `self.run()`

        If a given finite element problem fails, we do will try once again with
        relaxed options. It is recommended to go back and check the model for 
        better understanding of the issue.

        Finally, an explicit function of time on the right hand side is 
        prohibited. Please put this information into an input (fixed variable)
        instead.

        :param ConcreteModel tgt_mod: The original fully discretized model that we want to patch the information to.
        :param ConcreteModel src_mod: The undiscretized reference model.
        :param str init_con: The initial constraint name (corresponds to a Constraint object).
        :param list param_name: The param name list. (Each element must correspond to a pyomo Var)
        :param dict param_values: The corresponding values: `param_dict["param_name", "param_index"] = 49.7796`
        :param dict inputs: The input dictionary. Use this dictonary for single index (time) inputs
        :param dict inputs_sub: The multi-index dictionary. Use this dictionary for multi-index inputs.
        
        """
        #%%
        #self = r1.simulator.init
        
        testing = False
        
        if testing:
        
            from kipet.estimator_tools.fe_factory import FEInitialize
            self = FEInitialize(r1._s_model, r1._s_model.clone())
            self.param_name = ['P'] #param_name
            self.param_values = r1.simulator.param_dict #param_values
            self.inputs_sub = {'Dose': ['d_var']} #inputs_sub
            
        else:
            self.param_name = param_name
            self.param_values = param_values
            self.inputs_sub = inputs_sub
            
        #from kipet.estimator_tools.pyomo_simulator import PyomoSimulator
        #model_orig = r1._s_model
        #src_mod = model_orig.clone()
        
        self.__var = VariableNames()

        self.ip = SolverFactory(solver_path('ipopt'))
        
        self.ip.options['halt_on_ampl_error'] = 'yes'
        self.ip.options['print_user_options'] = 'yes'

        # This is the full simulation model from ReactionModel
        self.model_orig = model_orig
        
        # This is the cloned model that will be used to make the individual FEs - not discretized
        self.model_ref = src_mod.clone()

        # These are the fixed states causing headaches
        self.fixed_states = [] #fixed_states
        
        # self.param_name = param_name
        # self.param_values = param_values
        
        # # These are the dosing points
        # self.inputs_sub = inputs_sub
        print(f'{self.inputs_sub = }')

        self.time_independent_variables = []  #:Not indexed by time
        self.remaining_set_alg = {}

        # Is this necessary?
        self.volume_name = self.__var.volume_name
        if self.volume_name is None:
            raise ValueError('A volume name must exist')

        # This gets the full time_index
        time_index = None
        for i in self.model_ref.component_objects(ContinuousSet):
            time_index = i
            break
        if time_index is None:
            raise Exception('no continuous_set')
        
        print(f'{time_index = }')

        self.time_set = time_index.name
        print(f'{self.time_set = }')


        # print('attempting to delete')
        
        # to_delete = ['dZdt_deq_aug', 'dZdt_disc_eq', 'dXdt_deq_aug', 'dXdt_disc_eq']
        
        # for model_component in to_delete:
        
        #     if hasattr(self.model_ref, model_component):
        #         print(f'Deleting {model_component}')
        #         self.model_ref.del_component(model_component)
            
        
        # This gets the original model's time set
        model_original_time_set = getattr(self.model_orig, self.time_set)
        print(f'{model_original_time_set = }')
        
        # The discretization info from the original model
        self.ncp = model_original_time_set.get_discretization_info()['ncp']
        
        
        fe_l = model_original_time_set.get_finite_elements()
        self.model_times = model_original_time_set.data()
        self.fe_list = [fe_l[i + 1] - fe_l[i] for i in range(0, len(fe_l) - 1)]
        self.nfe = len(self.fe_list)

        print("Time sets")
        print(f'{model_original_time_set = }')
        print(f'{self.time_set = }')
        print(f'self.fe_l/{fe_l = }')
        self.fe_l = fe_l
        print(f'{self.fe_list = }')


        #### This should be moved to a method ####
        #
        # self = r1.simulator.init
        
        #: Re-construct the model with [0,1] time domain
        times = getattr(self.model_ref, self.time_set)
        self.times = times
        
        print(f'self.times/{times = }')
        
        # This changes the time-span to {0, 1}
        change_continuous_set(times, [0, 1])
        
        # cs = times
        # new_bounds = [0, 1]
        
       
        # from pyomo.environ import Constraint
        # from pyomo.core.base.param import Param
        # from pyomo.core.base.set import BoundsInitializer, SetProduct
        # from pyomo.core.base.var import Var
        # #from pyomo.dae.contset import ContinuousSet
        # from pyomo.dae.diffvar import DerivativeVar
        
        # cs.clear()
        # cs._init_domain._set = None
        # cs._init_domain._set = BoundsInitializer(new_bounds)
        # domain = cs._init_domain(cs.parent_block(), None)
        # cs._domain = domain
        # domain.parent_component().construct()
        
        # for bnd in cs.domain.bounds():
        #     if bnd is not None and bnd not in cs:
        #         cs.add(bnd)
        # cs._fe = sorted(cs)
        
        
      
        # print('Before')
        # print(self.model_ref.Z.display())
        # print(self.model_ref.dZdt.display())

        # Go through and clear the variables and constraints of the ref model (the one used here)
        for var in self.model_ref.component_objects(Var):
            print(var)
            print(len(var))
            var.clear()
            #var._constructed = False
            var.reconstruct()
            
            print(len(var))
            
        # for var in self.model_ref.component_objects(DerivativeVar):
        #     print(var)
        #     print(len(var))
        #     var.clear()
        #     var._constructed = False
        #     var.construct()
            
        #     print(len(var))

        for con in self.model_ref.component_objects(Constraint):
            #print(con in self.derivative_state_variables)
            
            print(con)
            print(len(con))
            con.clear()
            #con._constructed = False
            con.reconstruct()
            print(len(con))

        print('After')
        
        #%%

        all_vars = list(self.model_ref.component_data_objects(Var))
        all_cons = list(self.model_ref.component_data_objects(Constraint))
        print(len(all_vars))
        print(len(all_cons))
        
        #%%
        
        # for var in ['Z', 'X']:
        
        #     # v_info = var_class
        #     # var, model_set = model_pred_var_name[var_class.attr_class_set_name]
            
        #     # print(f'This is what you need: {var}')
            
        #     # if hasattr(model_set, 'ordered_data') and len(model_set.ordered_data()) == 0:
        #     #     continue
            
        #     # setattr(model, var, Var(model.alltime,
        #     #                               model_set,
        #     #                               initialize=1) 
        #     #         )    
        
        #     # for time, comp in getattr(model, var):
        #     #     if time == model.start_time.value:
                    
        #     #         getattr(model, var)[time, comp].value = v_info[comp].value
        #     model_pred_var_name = {
        #             'Z' : [self.__var.concentration_model, self.model_ref.mixture_components],
        #             'X' : [self.__var.state_model, self.model_ref.complementary_states],
        #                 }
        
        #     model_set = model_pred_var_name[var][1]
            
        #     # self.model_ref.del_component(f'{var}')      
            
        #     # setattr(self.model_ref, f'{var}', Var(cs,
        #     #                                       model_set,
        #     #                                       initialize=1),
        #     # )
            
            
        #     self.model_ref.del_component('d{var}dt')      
            
        #     setattr(self.model_ref, f'd{var}dt', DerivativeVar(getattr(self.model_ref, var),
        #                                                        wrt=cs)
        #     )
        
        
        
        #%%

        

        # self.model_ref.display(filename="selfmoddisc0.txt")
        #: Discretize
        d = TransformationFactory('dae.collocation')
        d.apply_to(self.model_ref, nfe=1, ncp=self.ncp, scheme='LAGRANGE-RADAU')

        #: Find out the differential variables
        self.state_variables = []
        self.derivative_state_variables = []

        for con in self.model_ref.component_objects(Constraint):
            name = con.name
            namel = name.split('_', 1)
            if len(namel) > 1:
                if namel[1] == "disc_eq":
                    realname = getattr(self.model_ref, namel[0])
                    self.derivative_state_variables.append(namel[0])
                    self.state_variables.append(realname.get_state_var().name)
                    
        # dXdt, dZdt
        print(f'{self.derivative_state_variables = }')
        # X, Z
        print(f'{self.state_variables = }')

        
        print(times.display())
        # times is the set of "times" (aka the collocation points) between 0 and 1
        self.model_ref.h_i = Param(times, mutable=True, default=1.0)  #: Length of finite element
        print(self.model_ref.h_i.display())

        # dZdt still has the end time of the original model at this point

        #: Modify the collocation equations to introduce h_i (the length of finite element)
        for i in self.derivative_state_variables:
            print(f'{i} in {self.derivative_state_variables}')
            
            # This is the constraint associated with the derivative variables
            con = getattr(self.model_ref, i + '_disc_eq')
            print(f'{con = }')
            #print(con.display())
            # This is the varaible object associated with i
            dv = getattr(self.model_ref, i)
            print(f'{dv = }')
            print(dv.display())
            
            e_dict = {}
            
            fun_tup = True
            for k in con.keys():
                print(f'in the con.keys loop: {k = }')
                
                if isinstance(k, tuple):
                    pass
                else:
                    k = (k,)
                    fun_tup = False
                e = con[k].expr.args[0]
                e_dict[k] = e * self.model_ref.h_i[k[0]] + dv[k] * (
                        1 - self.model_ref.h_i[k[0]]) == 0.0  #: As long as you don't clone
            if fun_tup:
                self.model_ref.add_component(i + "_deq_aug",
                                             Constraint(con.index_set(),
                                                        rule=lambda m, *j: e_dict[j] if j[0] > 0.0 else Constraint.Skip))
            else:
                self.model_ref.add_component(i + "_deq_aug",
                                             Constraint(con.index_set(),
                                                        rule=lambda m, j: e_dict[j] if j > 0.0 else Constraint.Skip))
            self.model_ref.del_component(con)
        
        #: Sets for iteration
        #: Differential variables
        self.remaining_set = {}
        for i in self.state_variables:
            dv = getattr(self.model_ref, i)
            if dv.index_set().name == times.name:  #: Just time set
                # print(i, 'here')
                self.remaining_set[i] = None
                continue
            
            print(f'{self.remaining_set = }')
            print(f'{dv = }')
            # set_i = dv._implicit_subsets  #: More than just time set
            # set_i = dv._index._implicit_subsets #Update for pyomo 5.6.8 KH.L
            set_i = identify_member_sets(dv)
            # set_i = identify_member_sets(dv.index_set())
            # print(f'set_i = {set_i}')
            remaining_set = set_i[1]
            for s in set_i[2:]:
                remaining_set *= s
            if isinstance(remaining_set, list):
                self.remaining_set[i] = remaining_set
            else:
                self.remaining_set[i] = []
                self.remaining_set[i].append(remaining_set)
                
        print(f'{self.remaining_set = }')
                
        #: Algebraic variables
        
        # This is most likely where the problem starts
        
        self.define_remaining_set()
                
        # The remaining set may interfere with the algebraics Y at some point leading to the wrong results
        
        # Remaining set is dXdt, dZdt, Dose, Y

        # This seems to be handling the initial conditions
        # Delete the initial conditions (we use .fix() instead)

        if init_con is not None:  
            initial_condition = getattr(self.model_ref, init_con)
            self.model_ref.del_component(initial_condition)

        self.fix_parameters()
        #: Fix initial conditions of state variables (Z and X)

        self.inputs = None
        self.input_remaining_set = {}

        self.fix_state_initial_conditions()
        self.fix_variables()
        self.load_fixed_states(0, init=True)

        (n, m) = reconcile_nvars_mequations(self.model_ref)
        if n != m:
            raise Exception("Inconsistent problem; n={}, m={}".format(n, m))
        else:
            print(f'Consistent problem: {n = }, {m = }')
            
        self.jump = False
        self.con_num = 0

        for i in self.model_ref.component_objects(Constraint):
            print(i)
            
            
        #print(stop)
            #%%
    # def dose_point_set_up(self):
        
    #     time_set_orig = getattr(self.model_orig, self.time_set)
        
    #     for model_var, dosing_point_list in self.dosing_points.items():

    #         for dosing_point in dosing_point_list:

    #             self.jump_fe, self.jump_cp = fe_cp(time_set_orig, dosing_point.time)
    #             comp_dict = self.make_comp_list()


    def define_remaining_set(self):
        """Defines the remaining set and the time independent variables
        
        Time independent variables are those without time indicies
        
        """
        for algebraic_variable in self.model_ref.component_objects(Var):

            print(f'{algebraic_variable.name = }')
            if algebraic_variable.name in self.state_variables:
                continue
            
            # Skip adding the time set (None in the algebraic_variable)
            if algebraic_variable.index_set().name == self.times.name:  #: Just time set
                self.remaining_set_alg[algebraic_variable.name] = None
                continue

            set_i = identify_member_sets(algebraic_variable)
            print(f'{set_i = }')
            if set_i is None or not self.times in set_i:
                self.time_independent_variables.append(algebraic_variable.name)  #: Not indexed by time!
                continue  #: if this happens we might be in trouble
            remaining_set = set_i[1]  #: Index by time and others
            for s in set_i[2:]:
                if s.name == self.times.name:
                    self.remaining_set_alg[algebraic_variable.name] = None
                    continue
                else:
                    remaining_set *= s
            if isinstance(remaining_set, list):
                self.remaining_set_alg[algebraic_variable.name] = remaining_set
            else:
                self.remaining_set_alg[algebraic_variable.name] = []
                self.remaining_set_alg[algebraic_variable.name].append(remaining_set)
                
        print(f'{self.remaining_set_alg = }')
        print(f'{self.time_independent_variables = }')
        
        return None
    

    def load_fixed_states(self, n_fe, init=False):
        """
        This method fixes the correct values for fixed states in the reference model
        """
        if hasattr(self.model_ref, self.__var.algebraic):
            model_var_obj_ref = getattr(self.model_ref, self.__var.algebraic)
            model_var_obj_org = getattr(self.model_orig, self.__var.algebraic)
            #for index, obj in getattr(self.model_ref, self.__var.algebraic).items():
            for alg in self.fixed_states:
                for i, t in enumerate(self.times):
                    # if i == 0 and not init:
                    #     continue
                    # print(alg)
                    # #for i, t in enumerate(self.times):
                    # print(f"START ITER {i}")
                    # print(i, t)
                    # print("the value in the ref")
                    # print(model_var_obj_ref[(t,) + (alg,)].value)
                    # print("the value in the orig at the fe start")
                    #print(model_var_obj_org[(self.model_times[n_fe*self.ncp + i],) + (alg,)].value)
                    model_var_obj_ref[(t,) + (alg,)].set_value(model_var_obj_org[(self.model_times[n_fe*self.ncp + i],) + (alg,)].value)
                    # print("END ITER")
                    #model_var_obj_ref.fix()
                    model_var_obj_ref[(t,) + (alg,)].fix()

                    #print(model_var_obj_ref[(t, alg)].value)

    def load_initial_conditions(self, init_cond=None):
        if not isinstance(init_cond, dict):
            raise Exception("init_cond must be a dictionary")

        for i in self.state_variables:
            dv = getattr(self.model_ref, i)
            ts = getattr(self.model_ref, self.time_set)  # self.model_ref.alltime
            for t in ts:
                for s in self.remaining_set[i]:
                    if s is None:
                        val = init_cond[i]  #: if you do not have an extra index, just put the value there
                        dv[t].set_value(val)
                        if t == 0:
                            if not dv[0].fixed:
                                dv[0].fix()
                        continue
                    for k in s:
                        val = init_cond[i, k]
                        k = k if isinstance(k, tuple) else (k,)
                        dv[(t,) + k].set_value(val)
                        if t == 0:
                            if not dv[(0,) + k].fixed:
                                dv[(0,) + k].fix()
                            
                            
    def fix_state_initial_conditions(self):
        """This fixes the initial xonditions for the state variables (X and Z)
        
        """
        for i in self.state_variables:
            state_variable = getattr(self.model_ref, i)
            
            if self.remaining_set[i] is None:
                state_variable[0].fix()
                
            for remaining_set in self.remaining_set[i]:
                for key in remaining_set:
                    key = key if isinstance(key, tuple) else (key,)
                    state_variable[(0,) + key].fix()
                    print(f'{state_variable[(0,) + key]}')
                    
        return None
    
    
    def fix_parameters(self):
        """This ensures that the model parameters are fixed
        
        """
        # This is a complicated way to fix parameters
        print(f'{self.param_name = }')
        if isinstance(self.param_name, list):  #: Time independent parameters
            print('self.param_name is a list')
        
            if self.param_values:
                if isinstance(self.param_values, dict):
                    for pname in self.param_name:
                        p = getattr(self.model_ref, pname)
                        for key in p.keys():
                            try:
                                val = self.param_values[pname, key]
                                p[key].set_value(val)
                            except KeyError:
                                raise Exception("Missing a key of the self.param_values\n"
                                                "Please provide all the required keys.\n"
                                                "missing: {}".format(key))
                            p[key].fix()
                else:
                    Exception("Arg self.param_values should be provided in a dictionary")
            else:
                Exception("Arg self.param_values should be provided in a dictionary")
                
                
        elif isinstance(self.param_name, str):
            if self.param_values:
                if isinstance(self.param_values, dict):
                    p = getattr(self.model_ref, self.param_name)
                    for key in p.keys():
                        try:
                            val = self.param_values[self.param_name, key]
                            p[key].set_value(val)
                        except KeyError:
                            raise Exception("Missing a key of the self.param_values\n"
                                            "Please provide all the required keys.\n"
                                            "missing: {}".format(key))
                        p[key].fix()
                        
        elif not self.param_name:
            pass
        
        else:
            raise Exception("wrong type for self.param_name")
            
        return None
    
                            
    def fix_variables(self):
        """This method fixes dosing points, time step changes, and model constatns
        
        """
        if self.inputs_sub is not None:
            print(self.inputs_sub)
            for key in self.inputs_sub.keys():
                model_var_obj = getattr(self.model_ref, key)

                for k in self.inputs_sub[key]:
                    if isinstance(k, str) or isinstance(k, int) or isinstance(k, tuple):
                        k = (k,) if not isinstance(k, tuple) else k
                    else:
                        raise RuntimeError("{} is not a valid index".format(k))

                    for t in self.times:
                        model_var_obj[(t,) + k].fix()

        if hasattr(self.model_ref, self.__var.time_step_change):
            for time_step in getattr(self.model_ref, self.__var.time_step_change):
                getattr(self.model_ref, self.__var.time_step_change)[time_step].fix()

        if hasattr(self.model_ref, self.__var.model_constant):
            for param, obj in getattr(self.model_ref, self.__var.model_constant).items():
                obj.fix()

        return None

    def march_forward(self, fe):
        """Moves forward with the simulation.

        This method performs the actions required for setting up the `fe-th` problem.

        Adjust inputs.
        Solve current problem.
        Patches tgt_model.
        Cycles initial conditions

        :param int fe: The corresponding finite element.

        :return: None

        """
        self.adjust_h(fe)
        if self.inputs or self.inputs_sub:
            self.load_input(fe)

        print(f"Currently {fe = }")
        #self.load_fixed_states(fe)
        #self.model_ref.Y.display()
        #self.model_ref.X.display()

        self.ip.options["print_level"] = 5  #: change this on demand
        # self.ip.options["start_with_resto"] = 'no'
        self.ip.options['bound_push'] = 1e-02
        
        for key, value in self.ip.options.items():
            print(f'{key}: {value}')
        
        # print(f'{self.model_ref.Y[0, "diff2"] = }')
        
        print("starting to solve")
        sol = self.ip.solve(self.model_ref, tee=True, symbolic_solver_labels=True)
        print("has been solved")

        # Try to redo it if it fails
        if sol.solver.termination_condition != TerminationCondition.optimal:
            self.ip.options["OF_start_with_resto"] = 'yes'

            sol = self.ip.solve(self.model_ref, tee=False, symbolic_solver_labels=True)
            if sol.solver.termination_condition != TerminationCondition.optimal:

                self.ip.options["OF_start_with_resto"] = 'no'
                self.ip.options["bound_push"] = 1E-02
                self.ip.options["OF_bound_relax_factor"] = 1E-05
                sol = self.ip.solve(self.model_ref, tee=True, symbolic_solver_labels=True)
                self.ip.options["OF_bound_relax_factor"] = 1E-08

                # It if fails twice, raise an error
                if sol.solver.termination_condition != TerminationCondition.optimal:
                    raise Exception("The current iteration was unsuccessful. Iteration :{}".format(fe))

        
        self.patch(fe)
        print('AFTER patch ##########################################################################')
        self.load_fixed_states(fe)
       #self.model_ref.Y.display()
        #self.model_ref.X.display()
        self.cycle_ics(fe)

        # print("AFTER\n\n####################################################")
        # model_var_obj_ref = getattr(self.model_ref, self.__var.algebraic)
        # if hasattr(self.model_ref, self.__var.algebraic):
        #     #for index, obj in getattr(self.model_ref, self.__var.algebraic).items():
        #     for alg in self.fixed_states:
        #         for i, t in enumerate(self.times):
        #             print(model_var_obj_ref[(t, alg)].value)

    def load_discrete_jump(self, dosing_points):
        """Method is used to define and load the places where discrete jumps are located, e.g.
        dosing points or external inputs.

        :param list dosing_points: A list of DosingPoint objects

        :return: None

        """
        self.jump = True
        self.dosing_points = dosing_points

        return None

    def cycle_ics(self, curr_fe):
        """Cycles the initial conditions of the initializing model.
        Take the values of states (initializing model) at t=last and patch them into t=0.
        Check: :ref:`<https://github.com/dthierry/cappresse/blob/pyomodae-david/nmpc_mhe/aux/utils.py>`_
        fe_cp function!

        :param int curr_fe: The current finite element

        :return: None

        """
        model_time_set = getattr(self.model_ref, self.time_set)
        t_last = t_ij(model_time_set, 0, self.ncp)

        for state_variable in self.state_variables:
            state_variable_object = getattr(self.model_ref, state_variable)
            
            for pyomo_set in self.remaining_set[state_variable]:
                if pyomo_set is None:
                    self.set_initial_condition_value([0], t_last, state_variable_object)
                else:
                    for k in pyomo_set:
                        k = k if isinstance(k, tuple) else (k,)                        
                        self.set_initial_condition_value((0,) + k, (t_last,) + k, state_variable_object)

    @staticmethod
    def set_initial_condition_value(index, time, state_variable_object):
                
        val = value(state_variable_object[time])
        # state_variable_object[index].set_value(val)
        state_variable_object[index].fix(val)
        
        return None

    def patch(self, fe):
        """ Take the current state of variables of the initializing model at fe and load it into the tgt_model
        Note that this will skip fixed variables as a safeguard.

        :param int fe: The current finite element to be patched (tgt_model).

        :return: None

        """
        print(f'In patch for fe = {fe}')
        
        time_set_ref = getattr(self.model_ref, self.time_set)
        time_set_orig = getattr(self.model_orig, self.time_set)

        for model_ref_var in self.model_ref.component_objects(Var, active=True):
            model_orig_var = getattr(self.model_orig, model_ref_var.name)
            
            #print(f'{model_ref_var.name = }')
            
            if model_ref_var.name in self.time_independent_variables:
                for k in model_ref_var.keys():
                    if model_ref_var[k].stale or model_ref_var[k].is_fixed():
                        continue
                    try:
                        val = model_ref_var[k].value
                    except ValueError:
                        pass
                    model_ref_var[k].set_value(val)
                continue
            #: From this point on all variables are indexed over time.
            if model_ref_var.name in self.state_variables:
                drs = self.remaining_set[model_ref_var.name]
            else:
                drs = self.remaining_set_alg[model_ref_var.name]
                #print(drs)

            for j in range(0, self.ncp + 1):

                t_tgt = t_ij(time_set_orig, fe, j)
                t_src = t_ij(time_set_ref, 0, j)

                #print(f'{t_tgt = }')
                #print(f'{t_src = }')

                if drs is None:
                    if model_ref_var[t_src].stale or model_ref_var[t_src].is_fixed():
                        continue
                    try:
                        val = model_ref_var[t_src].value
                    except ValueError:
                        print("Error at {}, {}".format(model_ref_var.name, t_src))
                    model_ref_var[t_tgt].set_value(val)
                    continue

                for k in drs:
                    # print(f'{k = }')
                    for key in k:
                        # print(f'{key = }')
                        
                        key = key if isinstance(key, tuple) else (key,)
                        if model_ref_var.name not in self.fixed_states:
                            if model_ref_var[(t_src,) + key].stale or model_ref_var[(t_src,) + key].is_fixed():
                                #print(f'{key = } is fixed')
                                continue
                            try:
                                val = value(model_ref_var[(t_src,) + key])
                            except ValueError:
                                print("Error at {}, {}".format(model_ref_var.name, (t_src,) + key))
                        model_orig_var[(t_tgt,) + key].set_value(val)

        if self.jump:

                    

            """This creates a new constraint forcing the variable at the
            specific time to be equal to step size provided in the dosing
            points. It creates the constraint and replaces the variable in the
            original ode equations.
            """
            for model_var, dosing_point_list in self.dosing_points.items():

                for dosing_point in dosing_point_list:

                    self.jump_fe, self.jump_cp = fe_cp(time_set_orig, dosing_point.time)
                    comp_dict = self.make_comp_list()

                    vs = ReplacementVisitor()

                    if fe == self.jump_fe + 1:

                        for comp_tuple in comp_dict:
                            model_var = comp_tuple[0]
                            comp = comp_tuple[1]
                            con_name = f'd{model_var}dt_disc_eq'
                            varname = f'{model_var}_dummy_{self.con_num}'
                            #conc_delta = self.concentration_calc(dosing_point)
                            conc_delta_obj = self.concentration_expr(dosing_point)
                            
                            # print(f'{comp = }')
                            # print(f'{conc_delta = }')
                            
                            # print(f'{dosing_point = }')
                           
                            """
                            # This is the constraint you want to change (add dummy for the model_var)
                            model_con_obj = getattr(self.model_orig, con_name)

                            # Adding some kind of constraint to the list
                            self.model_orig.add_component(f'{model_var}_dummy_eq_{self.con_num}_{comp}',
                                                          ConstraintList())
                            model_con_objlist = getattr(self.model_orig, f'{model_var}_dummy_eq_{self.con_num}_{comp}')

                            # Adding a variable (no set) with dummy name to model
                            self.model_orig.add_component(varname, Var([0]))

                            # vdummy is the var_obj of the Var you just made
                            vdummy = getattr(self.model_orig, varname)

                            # this is the variable that will replace the other
                            vs.change_replacement(vdummy[0])

                            # adding a parameter that is the jump at dosing_point.step (the size or change in the var)
                            self.model_orig.add_component(f'{model_var}_jumpdelta{self.con_num}_{comp}',
                                                          Param(initialize=conc_delta[comp]))

                            # This is the param you just made
                            jump_param = getattr(self.model_orig, f'{model_var}_jumpdelta{self.con_num}_{comp}')

                            # This is where the new concentrations need to be calculated - start with A
                            # jump_param is what needs to be modified

                            # Constraint setting the variable equal to the step size
                            # Can you make this handle the volume as well?
                            
                            exprjump = vdummy[0] - getattr(self.model_orig, model_var)[
                                (dosing_point.time,) + (comp,)] == jump_param
                            
                            Hard code here
                            
                            exprjump = vdummy[0] - getattr(self.model_orig, model_var)[
                                (dosing_point.time,) + (comp,)] == jump_param
                            """



                            # This is the constraint you want to change (add dummy for the model_var)
                            model_con_obj = getattr(self.model_orig, con_name)

                            # Adding some kind of constraint to the list
                            self.model_orig.add_component(f'{model_var}_dummy_eq_{self.con_num}_{comp}',
                                                          ConstraintList())
                            model_con_objlist = getattr(self.model_orig, f'{model_var}_dummy_eq_{self.con_num}_{comp}')

                            # Adding a variable (no set) with dummy name to model
                            self.model_orig.add_component(varname, Var([0]))

                            # vdummy is the var_obj of the Var you just made
                            vdummy = getattr(self.model_orig, varname)

                            # this is the variable that will replace the other
                            vs.change_replacement(vdummy[0])

                            # adding a parameter that is the jump at dosing_point.step (the size or change in the var)
                            
                            # This needs to be changed to a variable that handles the calculation
                            # self.model_orig.add_component(f'{model_var}_jumpdelta{self.con_num}_{comp}',
                            #                               Param(initialize=conc_delta[comp]))

                            # # This is the param you just made
                            # jump_param = getattr(self.model_orig, f'{model_var}_jumpdelta{self.con_num}_{comp}')

                            # This is where the new concentrations need to be calculated - start with A
                            # jump_param is what needs to be modified

                            # Constraint setting the variable equal to the step size
                            # Can you make this handle the volume as well?
                            
                            exprjump = vdummy[0] - getattr(self.model_orig, model_var)[
                                (dosing_point.time,) + (comp,)] == conc_delta_obj[comp] #jump_param





                            # Add the new constraint to the original model
                            self.model_orig.add_component(f'jumpdelta_expr{self.con_num}_{comp}',
                                                          Constraint(expr=exprjump))

                            # This adds the constraints over the collocation points
                            for kcp in range(1, self.ncp + 1):
                                curr_time = t_ij(time_set_orig, self.jump_fe + 1, kcp)
                                idx = (curr_time,) + (comp,)
                                model_con_obj[idx].deactivate()
                                var_expr = model_con_obj[idx].expr
                                
                                self.var_expr = var_expr
                                print(var_expr)
                                
                                suspect_var = var_expr.args[0].args[1].args[0].args[0].args[1]
                                vs.change_suspect(id(suspect_var))  #: who to replace
                                e_new = vs.dfs_postorder_stack(var_expr)  #: replace
                                model_con_obj[idx].set_value(e_new)
                                model_con_objlist.add(model_con_obj[idx].expr)

                            self.con_num += 1

    def make_comp_list(self):
        """Creates a list of tuples to pair model variables with component
        and volume variables
        
        :return list comp_dict: A list of tuples
        
        """
        comp_dict = []
        for comp in self.model_orig.mixture_components.keys():
            comp_dict.append((self.__var.concentration_model, comp))
        comp_dict.append((self.__var.state_model, self.volume_name))
        return comp_dict

    def concentration_calc(self, dosing_point):
        """This method calculates the changes in the concentration when 
        adding a volume of substance with specified concentrations of species
        
        :param DosingPoint dosing_point: Takes a dosing point object
        
        :return dict delta_conc: A dict of tuples with the component and 
          step change in concentration. This includes the volume step too.
        
        .. note::
            
            This only takes a single species at the moment. Use multiple dosing
            points if you need to add mixtures at the same point.
            
        """
        # This is not changing the volumes for the entire model after this point
        # This is a problem for later concentration calculations
        
        # try to add the concentration change as a constraint with the volume instead of the fixed value
        
        #print(f'{dosing_point = }')
        
        time_set_orig = getattr(self.model_orig, self.time_set)
        #print(f'{time_set_orig = }')

        # Get the current time point
        curr_time = t_ij(time_set_orig, self.jump_fe + 1, 1)
        #print(f'{curr_time = }')
        # Get the current volume
        vol = getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)].value

        #print(f'{vol = }')
        
        #print(getattr(self.model_orig, self.__var.state_model).display())
        #print(getattr(self.model_ref, self.__var.state_model).display())
        
        # Get the current concentrations
        conc = {}
        for comp in list(self.model_orig.mixture_components.keys()):
            conc[comp] = getattr(self.model_orig, self.__var.concentration_model)[(curr_time,) + (comp,)].value

        #print(f'{conc = }')
        # Calculate the moles of each substance at the current point
        moles = {}
        for comp in conc:
            moles[comp] = vol * conc[comp]

        conc_change = dosing_point.conc[0]
        vol_change = dosing_point.vol[0]

        # Add the dosing point to the moles
        moles[dosing_point.component] += conc_change * vol_change
        vol += vol_change
        delta_conc = {k: v / vol - conc[k] for k, v in moles.items()}
        delta_conc[self.volume_name] = vol_change
        
        #getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)].set_value(vol + vol_change)
        
        return delta_conc
    
    def concentration_expr(self, dosing_point):
        """This method calculates the changes in the concentration when 
        adding a volume of substance with specified concentrations of species
        
        :param DosingPoint dosing_point: Takes a dosing point object
        
        :return dict delta_conc: A dict of tuples with the component and 
          step change in concentration. This includes the volume step too.
        
        .. note::
            
            This only takes a single species at the moment. Use multiple dosing
            points if you need to add mixtures at the same point.
            
        """
        #model_orig = r1.p_model
        
        #print(f'{dosing_point = }')
        
        time_set_orig = getattr(self.model_orig, self.time_set)
        #print(f'{time_set_orig = }')

        # Get the current time point
        curr_time = t_ij(time_set_orig, self.jump_fe + 1, 1)

        curr_time = dosing_point.time

        #vol = getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)].value
        # Get the current volume
        vol = getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)].value
        vol_obj = getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)]
        #print(f'{curr_time = }')
        #print(f'{vol = }')
        #print(vol_obj.pprint())
        # Get the current concentrations
        conc = {}
        conc_obj = {}
        for comp in list(self.model_orig.mixture_components.keys()):
            conc[comp] = getattr(self.model_orig, self.__var.concentration_model)[(curr_time,) + (comp,)].value
            conc_obj[comp] = getattr(self.model_orig, self.__var.concentration_model)[(curr_time,) + (comp,)]

        #print(f'{conc = }')
        #print(f'{conc_obj = }')
        # Calculate the moles of each substance at the current point
        moles = {}
        moles_expr = {}
        for comp in conc:
            moles[comp] = vol * conc[comp]
            moles_expr[comp] = vol_obj * conc_obj[comp]

        conc_change = dosing_point.conc[0]
        vol_change = dosing_point.vol[0]

        # Add the dosing point to the moles
        moles[dosing_point.component] += conc_change * vol_change
        moles_expr[dosing_point.component] += conc_change * vol_change
        vol += vol_change
        vol_obj += vol_change
        
        delta_conc = {k: v / vol - conc[k] for k, v in moles.items()}
        delta_conc[self.volume_name] = vol_change
        
        delta_conc_obj = {k: v / vol_obj - conc_obj[k] for k, v in moles_expr.items()}
        delta_conc_obj[self.volume_name] = vol_change
        
        #print(delta_conc)
        #print(delta_conc_obj['A'].to_string())
        
        return delta_conc_obj

    def adjust_h(self, fe):
        """Adjust the h_i parameter of the initializing model.

        The initializing model goes from t=(0,1) so it needs to be scaled by the current time-step size.

        :param int fe: The current value of h_i

        :return: None

        """
        hi = getattr(self.model_ref, "h_i")
        time = getattr(self.model_ref, self.time_set)
        for t in time:
            hi[t].value = self.fe_list[fe]

    def run(self, resto_strategy="bound_relax"):
        """Runs the sequence of problems fe=0,nfe

        :param str resto_strategy: The restoration strategy for the march_forward algorithm

        :return: None

        """
        for i in range(0, len(self.fe_list)):
            self.march_forward(i)
            
        #print(getattr(self.model_orig, self.__var.state_model).display())
        #print(getattr(self.model_orig, 'Z').display())
        #print(getattr(self.model_ref, self.__var.state_model).display())

    def load_input(self, fe):
        """ Loads the current value of input from tgt_model into the initializing model at the current fe.

        :param int fe:  The current finite element to be loaded.

        :return: None

        """
        if self.inputs is not None:
            time_set_ref = getattr(self.model_ref, self.time_set)
            time_set_orig = getattr(self.model_orig, self.time_set)
            for i in self.inputs:
                p_data = getattr(self.model_orig, i)
                p_sim = getattr(self.model_ref, i)
                if self.input_remaining_set[i] is None:
                    for j in range(0, self.ncp + 1):
                        t = t_ij(time_set_orig, fe, j)
                        tsim = t_ij(time_set_ref, 0, j)
                        val = value(p_data[t])
                        p_sim[tsim].set_value(val)
                    continue
                for k in self.input_remaining_set[i]:
                    for key in k:
                        for j in range(0, self.ncp + 1):
                            t = t_ij(time_set_orig, fe, j)
                            tsim = t_ij(time_set_ref, 0, j)
                            val = value(p_data[(t,) + key])
                            p_sim[(tsim,) + key].set_value(val)

        # Here is where the jumps come in... (can this be done with a different var?)
        if self.inputs_sub is not None:
            time_set_ref = getattr(self.model_ref, self.time_set)
            time_set_orig = getattr(self.model_orig, self.time_set)

            for key in self.inputs_sub.keys():  # Y
                model_orig_var = getattr(self.model_orig, key)
                model_ref_var = getattr(self.model_ref, key)

                for sub_key in self.inputs_sub[key]:
                    sub_key = (sub_key,) if not isinstance(sub_key, tuple) else k

                    for j in range(0, self.ncp + 1):
                        t_orig = t_ij(time_set_orig, fe, j)
                        t_ref = t_ij(time_set_ref, 0, j)
                        val = model_orig_var[(t_orig,) + sub_key].value
                        model_ref_var[(t_ref,) + sub_key].set_value(val)

    def create_bounds(self, bound_dict):
        time_set_ref = getattr(self.model_ref, self.time_set)
        for v in bound_dict.keys():
            var = getattr(self.model_ref, v)
            varbnd = bound_dict[v]
            if not isinstance(varbnd, dict):
                raise RuntimeError("The entry for {} is not a dictionary".format(v))
            for t in time_set_ref:
                for k in varbnd.keys():
                    bnd = varbnd[k]
                    if not isinstance(k, tuple):
                        k = (k,)
                    var[(t,) + k].setlb(bnd[0])  #: Lower bound
                    var[(t,) + k].setub(bnd[1])  #: Upper bound

    def clear_bounds(self):
        for v in self.model_ref.component_data_objects(Var):
            v.setlb(None)
            v.setub(None)


def t_ij(time_set, i, j):
    # type: (ContinuousSet, int, int) -> float
    """Return the corresponding time(continuous set) based on the i-th finite element and j-th collocation point
    From the NMPC_MHE framework by @dthierry.

    :param ContinuousSet time_set: Parent Continuous set
    :param int i: finite element
    :param int j: collocation point

    :return: Corresponding index of the ContinuousSet
    :rtype: float

    """
    if i < time_set.get_discretization_info()['nfe']:
        h = time_set.get_finite_elements()[i + 1] - time_set.get_finite_elements()[i]  #: This would work even for 1 fe
    else:
        h = time_set.get_finite_elements()[i] - time_set.get_finite_elements()[i - 1]  #: This would work even for 1 fe
    tau = time_set.get_discretization_info()['tau_points']
    fe = time_set.get_finite_elements()[i]
    time = fe + tau[j] * h
    return round(time, 6)


def write_nl(d_mod, filename=None):
    """
    Write the nl file

    :param ConcreteModel d_mod: the model of interest.

    :return str cwd: The current working directory.

    """
    if not filename:
        filename = d_mod.name + '.nl'
    d_mod.write(filename, format=ProblemFormat.nl,
                io_options={"symbolic_solver_labels": True})
    cwd = getcwd()
    # print("nl file {}".format(cwd + "/" + filename))
    return cwd


def reconcile_nvars_mequations(d_mod):
    """
    Compute the actual number of variables and equations in a model by reading the relevant line at the nl file.

    :param ConcreteModel d_mod: the model of interest.

    :return tuple: The number of variables and the number of constraints.

    """
    fullpth = getcwd()
    fullpth += "/_reconciled.nl"
    write_nl(d_mod, filename=fullpth)
    with open(fullpth, 'r') as nl:
        lines = nl.readlines()
        line = lines[1]
        newl = line.split()
        nvar = int(newl[0])
        meqn = int(newl[1])
        nl.close()

    return (nvar, meqn)


def disp_vars(model, file):
    """Helper function for debugging

    :param ConcreteModel model: the model of interest.
    :param str file: Destination text file.

    :return: None

    """
    with open(file, 'w') as f:
        for c in model.component_objects(Var):
            c.pprint(ostream=f)
        f.close()


def fe_cp(time_set, feedtime):
    """Return the corresponding fe and cp for a given time

    :param ContinuousSet time_set: The time index
    :param float feedtime: The time of the dosing point

    :return: tuple of the finite element and the collocation point

    """
    fe_l = time_set.get_lower_element_boundary(feedtime)
    fe = None
    j = 0
    for i in time_set.get_finite_elements():
        if fe_l == i:
            fe = j
            break
        j += 1
    h = time_set.get_finite_elements()[1] - time_set.get_finite_elements()[0]
    tauh = [i * h for i in time_set.get_discretization_info()['tau_points']]
    j = 0  #: Watch out for LEGENDRE
    cp = None
    for i in tauh:
        if round(i + fe_l, 6) == feedtime:
            cp = j
            break
        j += 1
    return fe, cp


def identify_member_sets(model_var_obj):
    """Identifies the index sets of the given variable

    :param GeneralVar model_var_obj: The variable object of the model

    :return: None or the list of indices

    """
    index_list = get_index_sets(model_var_obj)

    if len(index_list) > 1:
        return index_list
    else:
        return None
