#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 10:21:44 2021

@author: kevinmcbride
"""

#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import pyomo.common.unittest as unittest
import os

from pyomo.contrib.pynumero.dependencies import (
    numpy as np, numpy_available, scipy_available
)
if not (numpy_available and scipy_available):
    raise unittest.SkipTest("Pynumero needs scipy and numpy to run NLP tests")

from pyomo.contrib.pynumero.asl import AmplInterface
if not AmplInterface.available():
    raise unittest.SkipTest(
        "Pynumero needs the ASL extension to run NLP tests")

import pyomo.environ as pyo
from pyomo.contrib.pynumero.interfaces.pyomo_nlp import PyomoNLP
from pyomo.contrib.pynumero.interfaces.nlp_projections import RenamedNLP, ProjectedNLP



def create_pyomo_model():
    m = pyo.ConcreteModel()
    m.x = pyo.Var(range(3), bounds=(-10,10), initialize={0:1.0, 1:2.0, 2:4.0})

    m.obj = pyo.Objective(expr=m.x[0]**2 + m.x[0]*m.x[1] + m.x[0]*m.x[2] + m.x[2]**2)

    m.con1 = pyo.Constraint(expr=m.x[0]*m.x[1] + m.x[0]*m.x[2] == 4)
    m.con2 = pyo.Constraint(expr=m.x[0] + m.x[2] == 4)

    return m

m = create_pyomo_model()




#%%
def rule_fix_global_parameters(m, exp, param):
    
    for key, val in combined_model.map_exp_to_count.items():
        if param in self.global_params and param in getattr(combined_model.experiment[exp], self.__var.model_parameter):
            return getattr(combined_model.experiment[exp], self.__var.model_parameter)[param] - getattr(combined_model, global_param_name)[param] == 0
        else:
            return Constraint.Skip

set_fixed_params=set()
for exp in self.experiments:
    for param, param_obj in getattr(combined_model.experiment[exp], self.__var.model_parameter).items():
        if param_obj.is_fixed():
            set_fixed_params.add(param)
    
if len(set_fixed_params) > 0:
    print(f'# MEE: The fixed parameters are:\n{set_fixed_params}')

set_params_across_blocks = self.all_params.difference(set_fixed_params)
combined_model.parameter_linking = Constraint(self.experiments, set_params_across_blocks, rule = rule_fix_global_parameters)

#%%
# m = r1.p_model

# nlp = PyomoNLP(m)

nlp = r1._nlp
x_indx = nlp.get_primal_indices([r1.p_model.P['k1'], r1.p_model.P['k2']])


nlp.pyomo_model().d['k1'].set_value(1)
nlp.pyomo_model().d['k2'].set_value(1)

print(f'{nlp.get_primals()[x_indx] = }')
print(nlp.pyomo_model().P.display())
print(nlp.pyomo_model().d.display())

var_indx = nlp.get_primal_indices([getattr(r1.p_model, 'P')])
current_primals = nlp.get_primals()
current_primals[var_indx] = [1, 1]
nlp.set_primals(current_primals)
print(f'{nlp.get_primals()[x_indx] = }')
# J = projected_nlp.evaluate_jacobian()
# denseJ = J.todense()

# H = projected_nlp.evaluate_hessian_lag()
# denseH = H.todense()
try:
    del projected_nlp
finally:
    pass

projected_nlp = ProjectedNLP(nlp, nlp.primals_names())
print(f'{projected_nlp.get_primals()[x_indx] = }')
cy_nlp = CyIpoptNLP(projected_nlp)
# cy_nlp = CyIpoptNLP(nlp)


csolve = CyIpoptSolver(cy_nlp, 
                       options = {'linear_solver': 'ma57',
                                  'hsllib': 'libcoinhsl.dylib'})

r = csolve.solve(tee=True)

print(f'{r[0][var_indx] = }')
print(f'{nlp.get_primals()[x_indx] = }')

#%%

rd = r[1]

rd['x']


# I assume this is updating the same model as above - this means that it should
# be working for this 
var_indx = nlp.get_primal_indices([getattr(r1.p_model, 'P')])
current_primals = nlp.get_primals()
current_primals[var_indx] = [1, 1]
projected_nlp = ProjectedNLP(nlp, nlp.primals_names())

nlp.pyomo_model().d['k1'].set_value(1)
nlp.pyomo_model().d['k2'].set_value(1)

nlp.pyomo_model().P['k1'].set_value(1)
nlp.pyomo_model().P['k2'].set_value(1)

rd['x'][x_indx[0]] = 1
rd['x'][x_indx[1]] = 1

rd['x'][x_indx[0]] = 1
rd['x'][x_indx[1]] = 1

# rd['x'][0] = 1
# rd['x'][1] = 2

nlp.set_primals(rd['x'])
print(f'{nlp.get_primals()[x_indx] = }')
print(f'{projected_nlp.get_primals()[x_indx] = }')

projected_nlp_2 = ProjectedNLP(nlp, nlp.primals_names())
print(f'{projected_nlp_2.get_primals()[x_indx] = }')

cy_nlp_2 = CyIpoptNLP(projected_nlp_2)
csolve_2 = CyIpoptSolver(cy_nlp_2, 
                       options = {'linear_solver': 'ma57',
                                  'hsllib': 'libcoinhsl.dylib'})
r_2 = csolve_2.solve(tee=True)

# How to get projections to work?
print(f'{r_2[0][x_indx] = }')

#%%
    
    
# m = create_pyomo_model()
# nlp = PyomoNLP(m)
# projected_nlp = ProjectedNLP(nlp, ['x[0]', 'x[1]', 'x[2]'])
# expected_names = ['x[0]', 'x[1]', 'x[2]']
# # self.assertEqual(projected_nlp.primals_names(), expected_names)
# # self.assertTrue(np.array_equal(projected_nlp.get_primals(),
# #                                np.asarray([1.0, 2.0, 4.0])))
# # self.assertTrue(np.array_equal(projected_nlp.evaluate_grad_objective(),
# #                                np.asarray([8.0, 1.0, 9.0])))
# # self.assertEqual(projected_nlp.nnz_jacobian(), 5)
# # self.assertEqual(projected_nlp.nnz_hessian_lag(), 6)

# J = projected_nlp.evaluate_jacobian()
# # self.assertEqual(len(J.data), 5)
# denseJ = J.todense()
# expected_jac = np.asarray([[6.0, 1.0, 1.0],[1.0, 0.0, 1.0]])
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# # test the use of "out"
# J = 0.0*J
# projected_nlp.evaluate_jacobian(out=J)
# denseJ = J.todense()
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# H = projected_nlp.evaluate_hessian_lag()
# # self.assertEqual(len(H.data), 6)
# expectedH = np.asarray([[2.0, 1.0, 1.0],[1.0, 0.0, 0.0], [1.0, 0.0, 2.0]])
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # test the use of "out"
# H = 0.0*H
# projected_nlp.evaluate_hessian_lag(out=H)
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # now test a reordering
# projected_nlp = ProjectedNLP(nlp, ['x[0]', 'x[2]', 'x[1]'])
# expected_names = ['x[0]', 'x[2]', 'x[1]']
# # self.assertEqual(projected_nlp.primals_names(), expected_names)
# # self.assertTrue(np.array_equal(projected_nlp.get_primals(), np.asarray([1.0, 4.0, 2.0])))
# # self.assertTrue(np.array_equal(projected_nlp.evaluate_grad_objective(),
# #                                np.asarray([8.0, 9.0, 1.0])))
# # self.assertEqual(projected_nlp.nnz_jacobian(), 5)
# # self.assertEqual(projected_nlp.nnz_hessian_lag(), 6)

# J = projected_nlp.evaluate_jacobian()
# # self.assertEqual(len(J.data), 5)
# denseJ = J.todense()
# expected_jac = np.asarray([[6.0, 1.0, 1.0],[1.0, 1.0, 0.0]])
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# # test the use of "out"
# J = 0.0*J
# projected_nlp.evaluate_jacobian(out=J)
# denseJ = J.todense()
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# H = projected_nlp.evaluate_hessian_lag()
# # self.assertEqual(len(H.data), 6)
# expectedH = np.asarray([[2.0, 1.0, 1.0],[1.0, 2.0, 0.0], [1.0, 0.0, 0.0]])
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # test the use of "out"
# H = 0.0*H
# projected_nlp.evaluate_hessian_lag(out=H)
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # now test an expansion
# projected_nlp = ProjectedNLP(nlp, ['x[0]', 'x[2]', 'y', 'x[1]'])
# expected_names = ['x[0]', 'x[2]', 'y', 'x[1]']
# # self.assertEqual(projected_nlp.primals_names(), expected_names)
# np.testing.assert_equal(projected_nlp.get_primals(),np.asarray([1.0, 4.0, np.nan, 2.0]))

# # self.assertTrue(np.array_equal(projected_nlp.evaluate_grad_objective(),
# #                                np.asarray([8.0, 9.0, 0.0, 1.0])))
# # self.assertEqual(projected_nlp.nnz_jacobian(), 5)
# # self.assertEqual(projected_nlp.nnz_hessian_lag(), 6)

# J = projected_nlp.evaluate_jacobian()
# # self.assertEqual(len(J.data), 5)
# denseJ = J.todense()
# expected_jac = np.asarray([[6.0, 1.0, 0.0, 1.0],[1.0, 1.0, 0.0, 0.0]])
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# # test the use of "out"
# J = 0.0*J
# projected_nlp.evaluate_jacobian(out=J)
# denseJ = J.todense()
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# H = projected_nlp.evaluate_hessian_lag()
# # self.assertEqual(len(H.data), 6)
# expectedH = np.asarray([[2.0, 1.0, 0.0, 1.0],[1.0, 2.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]])
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # test the use of "out"
# H = 0.0*H
# projected_nlp.evaluate_hessian_lag(out=H)
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # now test an expansion
# projected_nlp = ProjectedNLP(nlp, ['x[0]', 'x[2]'])
# expected_names = ['x[0]', 'x[2]']
# # self.assertEqual(projected_nlp.primals_names(), expected_names)
# np.testing.assert_equal(projected_nlp.get_primals(),np.asarray([1.0, 4.0]))

# # self.assertTrue(np.array_equal(projected_nlp.evaluate_grad_objective(),
# #                                np.asarray([8.0, 9.0])))
# # self.assertEqual(projected_nlp.nnz_jacobian(), 4)
# # self.assertEqual(projected_nlp.nnz_hessian_lag(), 4)

# J = projected_nlp.evaluate_jacobian()
# # self.assertEqual(len(J.data), 4)
# denseJ = J.todense()
# expected_jac = np.asarray([[6.0, 1.0],[1.0, 1.0]])
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# # test the use of "out"
# J = 0.0*J
# projected_nlp.evaluate_jacobian(out=J)
# denseJ = J.todense()
# # self.assertTrue(np.array_equal(denseJ, expected_jac))

# H = projected_nlp.evaluate_hessian_lag()
# # self.assertEqual(len(H.data), 4)
# expectedH = np.asarray([[2.0, 1.0],[1.0, 2.0]])
# denseH = H.todense()
# # self.assertTrue(np.array_equal(denseH, expectedH))

# # test the use of "out"
# H = 0.0*H
# projected_nlp.evaluate_hessian_lag(out=H)
# denseH = H.todense()
        # self.assertTrue(np.array_equal(denseH, expectedH))

    
    