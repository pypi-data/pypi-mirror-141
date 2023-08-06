#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 12:33:35 2021

@author: kevinmcbride
"""
#%%
model = r1._s_model
from pyomo.contrib.incidence_analysis.util import solve_strongly_connected_components
import pyomo.environ as pyo
solver = pyo.SolverFactory("ipopt")
solve_strongly_connected_components(m, solver, solve_kwds={"tee": True})