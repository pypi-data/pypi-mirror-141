#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:13:54 2021

@author: kevinmcbride
"""

"""This creates a new constraint forcing the variable at the
specific time to be equal to step size provided in the dosing
points. It creates the constraint and replaces the variable in the
original ode equations.
"""
from pyomo.core import Var, Param, Constraint, ConstraintList
from pyomo.dae import ContinuousSet

from kipet.model_tools.visitor_classes import ReplacementVisitor
from kipet.calculation_tools.helper import DosingPoint

from kipet.general_settings.variable_names import VariableNames
__var = VariableNames()
#%%
def set_up_jumps(model_orig, dosing_points):

    #%%
    
    #del model_orig
#    model_orig = r1.p_model
#    dosing_points = {'Z': [DosingPoint('A', 5, (10, 'molar'), (0.1, 'liter'))]}

    time_index = None
    for i in model_orig.component_objects(ContinuousSet):
        time_index = i
        break
    if time_index is None:
        raise Exception('no continuous_set')
    
    print(f'{time_index = }')

    time_set = time_index.name
    print(f'{time_set = }')
    
    time_set_orig = getattr(model_orig, time_set)
    
    ttgt = getattr(model_orig, time_set)
    ncp = ttgt.get_discretization_info()['ncp']
    # fe_l = ttgt.get_finite_elements()
    # fe_list = [fe_l[i + 1] - fe_l[i] for i in range(0, len(fe_l) - 1)]
    # ncp = ttgt.get_discretization_info()['ncp']
    
    con_num = 0

    # Change to only address the FEs for the dosing points
    #for fe in range(0, len(fe_list)):

        
        
    for model_var, dosing_point_list in dosing_points.items():
    
        for dosing_point in dosing_point_list:
    
            jump_fe, jump_cp = fe_cp(time_set_orig, dosing_point.time)
            comp_dict = make_comp_list(model_orig)        
            #conc_delta = concentration_calc(model_orig, time_set, jump_fe, dosing_point)
            conc_delta_obj = concentration_expr(model_orig, time_set, jump_fe, dosing_point)
    
            #if fe == jump_fe + 1:
    
            vs = ReplacementVisitor()            

            for comp_tuple in comp_dict:
                model_var = comp_tuple[0]
                comp = comp_tuple[1]
                con_name = f'd{model_var}dt_disc_eq'
                varname = f'{model_var}_dummy_{con_num}'
                
                #print(conc_delta)

                # This is the constraint you want to change (add dummy for the model_var)
                model_con_obj = getattr(model_orig, con_name)

                # Adding some kind of constraint to the list
                model_orig.add_component(f'{model_var}_dummy_eq_{con_num}_{comp}', ConstraintList())
                model_con_objlist = getattr(model_orig, f'{model_var}_dummy_eq_{con_num}_{comp}')

                # Adding a variable (no set) with dummy name to model
                model_orig.add_component(varname, Var([0]))

                # vdummy is the var_obj of the Var you just made
                vdummy = getattr(model_orig, varname)

                # this is the variable that will replace the other
                vs.change_replacement(vdummy[0])

                # adding a parameter that is the jump at dosing_point.step (the size or change in the var)
                # model_orig.add_component(f'{model_var}_jumpdelta{con_num}_{comp}',
                #                               Param(initialize=conc_delta[comp]))

                # # This is the param you just made
                # jump_param = getattr(model_orig, f'{model_var}_jumpdelta{con_num}_{comp}')

                # This is where the new concentrations need to be calculated - start with A
                # jump_param is what needs to be modified

                # Constraint setting the variable equal to the step size
                exprjump = vdummy[0] - getattr(model_orig, model_var)[
                    (dosing_point.time,) + (comp,)] == conc_delta_obj[comp] #jump_param

                # Add the new constraint to the original model
                model_orig.add_component(f'jumpdelta_expr{con_num}_{comp}',
                                              Constraint(expr=exprjump))

                for kcp in range(1, ncp + 1):
                    curr_time = t_ij(time_set_orig, jump_fe + 1, kcp)
                    idx = (curr_time,) + (comp,)
                    model_con_obj[idx].deactivate()
                    var_expr = model_con_obj[idx].expr
                    suspect_var = var_expr.args[0].args[1].args[0].args[0].args[1]
                    vs.change_suspect(id(suspect_var))  #: who to replace
                    e_new = vs.dfs_postorder_stack(var_expr)  #: replace
                    model_con_obj[idx].set_value(e_new)
                    model_con_objlist.add(model_con_obj[idx].expr)

                con_num += 1
                    
                
    exprjump.to_string()
                
 #%%                   
def make_comp_list(model_orig):
    """Creates a list of tuples to pair model variables with component
    and volume variables
    
    :return list comp_dict: A list of tuples
    
    """
    volume_name = 'V'
    
    
    comp_dict = []
    for comp in model_orig.mixture_components.keys():
        comp_dict.append((__var.concentration_model, comp))
    comp_dict.append((__var.state_model, volume_name))
    return comp_dict

# def concentration_calc(model_orig, time_set, jump_fe, dosing_point):
#     """This method calculates the changes in the concentration when 
#     adding a volume of substance with specified concentrations of species
    
#     :param DosingPoint dosing_point: Takes a dosing point object
    
#     :return dict delta_conc: A dict of tuples with the component and 
#       step change in concentration. This includes the volume step too.
    
#     .. note::
        
#         This only takes a single species at the moment. Use multiple dosing
#         points if you need to add mixtures at the same point.
        
#     """
#     print(f'{dosing_point = }')
    
#     volume_name = 'V'
#     time_set_orig = getattr(model_orig, time_set)
#     print(f'{time_set_orig = }')

#     # Get the current time point
#     curr_time = t_ij(time_set_orig, jump_fe + 1, 1)

#     #vol = getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)].value
#     # Get the current volume
#     vol = getattr(model_orig, __var.state_model)[(curr_time,) + (volume_name,)].value
#     print(f'{curr_time = }')
#     print(f'{vol = }')
#     # Get the current concentrations
#     conc = {}
#     for comp in list(model_orig.mixture_components.keys()):
#         conc[comp] = getattr(model_orig, __var.concentration_model)[(curr_time,) + (comp,)].value

#     print(f'{conc = }')
#     # Calculate the moles of each substance at the current point
#     moles = {}
#     for comp in conc:
#         moles[comp] = vol * conc[comp]

#     conc_change = dosing_point.conc[0]
#     vol_change = dosing_point.vol[0]

#     # Add the dosing point to the moles
#     moles[dosing_point.component] += conc_change * vol_change
#     vol += vol_change
#     delta_conc = {k: v / vol - conc[k] for k, v in moles.items()}
#     delta_conc[volume_name] = vol_change

#     return delta_conc   


def concentration_expr(model_orig, time_set, jump_fe, dosing_point):
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
    
    volume_name = 'V'
    time_set_orig = getattr(model_orig, time_set)
    #print(f'{time_set_orig = }')

    # Get the current time point
    curr_time = t_ij(time_set_orig, jump_fe + 1, 1)
    curr_time = dosing_point.time

    #vol = getattr(self.model_orig, self.__var.state_model)[(curr_time,) + (self.volume_name,)].value
    # Get the current volume
    vol = getattr(model_orig, __var.state_model)[(curr_time,) + (volume_name,)].value
    vol_obj = getattr(model_orig, __var.state_model)[(curr_time,) + (volume_name,)]
    #print(f'{curr_time = }')
    #print(f'{vol = }')
    #print(vol_obj.pprint())
    # Get the current concentrations
    conc = {}
    conc_obj = {}
    for comp in list(model_orig.mixture_components.data()):
        conc[comp] = getattr(model_orig, __var.concentration_model)[(curr_time,) + (comp,)].value
        conc_obj[comp] = getattr(model_orig, __var.concentration_model)[(curr_time,) + (comp,)]

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
    delta_conc[volume_name] = vol_change
    
    delta_conc_obj = {k: v / vol_obj - conc_obj[k] for k, v in moles_expr.items()}
    delta_conc_obj[volume_name] = vol_change
    
    #print(delta_conc)
    #print(delta_conc_obj)
    
    return delta_conc_obj
   #%%                 
def fe_cp(time_set, feedtime):
    """Return the corresponding fe and cp for a given time

    :param ContinuousSet time_set: The time index
    :param float feedtime: The time of the dosing point

    :return: tuple of the finite element and the collocation point

    """
    
    #feedtime = 5
    #time_set = time_set_orig
    

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
        
    #    print(i  + fe_l)
        
        if round(i + fe_l, 6) == feedtime:
            cp = j
            break
        j += 1
        
    #print(f'{fe = }')
    #print(f'{cp = }')
        
    return fe, cp
                    
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
                    
       #%%         