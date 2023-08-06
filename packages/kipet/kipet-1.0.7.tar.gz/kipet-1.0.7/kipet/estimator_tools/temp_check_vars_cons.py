#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 13:56:58 2021

@author: kevinmcbride
"""
#%%
from pyomo.core.base.var import Var
from pyomo.core.base.constraint import Constraint
from pyomo.common.collections import ComponentSet
from pyomo.dae.flatten import flatten_dae_components
from pyomo.util.subsystems import (
    generate_subsystem_blocks,
    TemporarySubsystemManager,
)
from pyomo.core.expr.visitor import identify_variables

from pyomo.contrib.incidence_analysis import IncidenceGraphInterface

model = r1._s_model
#model = lab.reaction_models['PO-1'].p_model

all_vars = list(model.component_data_objects(Var))
all_cons = list(model.component_data_objects(Constraint, active=True))



from pyomo.dae import ContinuousSet

include_scalar_cons=True

time_index = None
for i in model.component_objects(ContinuousSet):
    time_index = i
    break
if time_index is None:
    raise Exception('No ContinuousSet')
time_set = time_index.name

time = getattr(model, time_set)

scalar_vars, dae_vars = flatten_dae_components(model, time, Var)
scalar_cons, dae_cons = flatten_dae_components(model, time, Constraint)

print(f'{len(all_vars) = }')
print(f'{len(scalar_vars) = }')
print(f'{len(all_cons) = }')
print(f'{len(scalar_cons) = }')
print(f'{len(dae_cons) = }')

all_vars_names = [var.name for var in all_vars]

print(f'DAE vars: {len(all_vars) - len(scalar_vars)}')

print(f'Difference in vars and cons is: {len(all_vars) - len(scalar_vars) - len(all_cons)}')

def _filter_duplicates(comps):
    seen = set()
    for comp in comps:
        if id(comp) not in seen:
            seen.add(id(comp))
            yield comp

subsystem_cons = [list(_filter_duplicates(
    con[t] for con in dae_cons if t in con and con.active and con[t].active
)) for t in time
]
if include_scalar_cons:
    # Add scalar constraints; These presumably specify initial conditions
    subsystem_cons[0] += scalar_cons

# Then get variables in those constraints
con_vars = dict()
seen = set()
vars_in_cons = []
for i, t in enumerate(time):
    con_vars[t] = ComponentSet()
    for con in subsystem_cons[i]:
        for var in identify_variables(con.expr, include_fixed=False):
            con_vars[t].add(var)
            if id(var) not in seen:
                seen.add(id(var))
                vars_in_cons.append(var)
                
# There must be a cleaner way of doing this
active_cons = list(model.component_data_objects(Constraint, active=True))
con_names = [con.name for con in active_cons]
print(f'{len(active_cons) = }')
print(f'{len(vars_in_cons) = }')

vars_in_cons_set = set([s.name for s in vars_in_cons])
scalar_vars_set = set([s.name for s in scalar_vars])
active_scalar_vars = list(vars_in_cons_set.intersection(scalar_vars_set))

subsystem_vars = [list(_filter_duplicates(
    var[t] for var in dae_vars if t in var and var[t] in con_vars[t]
)) for t in time
]
if include_scalar_cons:
    for var in vars_in_cons:
        if var.name in active_scalar_vars:
            # Add scalar constraints; These presumably specify initial conditions
            subsystem_vars[0] += [var]

subsystems = [
    (cons, vars) for cons, vars in zip(subsystem_cons, subsystem_vars)
]

#%%
cons1, vars1 = subsystems[1]

cn = [c.name for c in cons1]
vn = [v.name for v in vars1]

print('cons')
for con in cons1:
    print(con.name)
    
print('\nvars')
for var in vars1:
    print(var.name)

#%%
for sub in subsystems:
    print(len(sub[0]), len(sub[1]))

"""

# New method failing
len(all_vars) = 1602
len(scalar_vars) = 92
len(all_cons) = 1355
len(scalar_cons) = 4
len(dae_cons) = 9
DAE vars: 1510
Difference in vars and cons is: 155


# Old method working - 20
len(all_vars) = 1606
len(scalar_vars) = 96
len(all_cons) = 1359
len(scalar_cons) = 20
len(dae_cons) = 9
DAE vars: 1510
Difference in vars and cons is: 151

New method working - 7
len(all_vars) = 801
len(scalar_vars) = 97
len(all_cons) = 701
len(scalar_cons) = 5
len(dae_cons) = 8
DAE vars: 704
Difference in vars and cons is: 3

Old method working- 7 
len(all_vars) = 801
len(scalar_vars) = 97
len(all_cons) = 701
len(scalar_cons) = 5
len(dae_cons) = 8
DAE vars: 704
Difference in vars and cons is: 3

Old working 7b:
    len(all_vars) = 5532
    len(scalar_vars) = 322
    len(all_cons) = 4685
    len(scalar_cons) = 4
    len(dae_cons) = 9
    DAE vars: 5210
    Difference in vars and cons is: 525
    
    
New not working 7b:
    ValueError: block_triangularize does not currently support 
    non-square matrices. Got matrix with shape (4685, 5206).
    
    l
    

"""