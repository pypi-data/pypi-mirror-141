import numpy as np
import pandas as pd


class OuterProblem(object):
    """ Define the outerproblem of the NSD

    This has the appropriate structure for checking if the model has already been
    updated.

    """
    def __init__(self, nlp, outervars, outervars_indices):
        
        self.nlp = nlp # This is the object that holds all of the functions needed to evaluate the problem (NSD)
        self.nfev = 0
        self.ngev = 0
        self.nhev = 0
        self.ncev = 0
        self.njev = 0
        self.x = self.nlp.get_primals()
        self.outervars = {v.name: v for v in outervars}
        self.outervars_indices = outervars_indices
        self.duals = self.nlp.get_duals()
        self.nx = self.nlp.n_primals()
        self.nc = self.nlp.n_constraints()
        self.obj_factor = 1.0 
        self.f_updated = False
        self.g_updated = False
        self.H_updated = False
        self.c_updated = False
        self.J_updated = False

        # Objective function evaluation
        def fun_wrapped():
            self.nfev += 1
            return self.nlp.evaluate_objective()

        def update_fun():
            self.f = fun_wrapped()
        
        self._update_fun_impl = update_fun
        self._update_fun()

        # Gradient evaluation
        def grad_wrapped():
            self.ngev += 1
            return self.nlp.evaluate_grad_objective()

        def update_grad():
            self.g = grad_wrapped()
        
        self._update_grad_impl = update_grad
        self._update_grad()

        # Hessian evaluation
        def hess_wrapped():
            self.nhev += 1
            return self.nlp.evaluate_hessian_lag().todense()

        def update_hess():
            self.H = hess_wrapped()

        self._update_hess_impl = update_hess
        self._update_hess()

        # Constraints evaluation
        def con_wrapped():
            self.ncev += 1
            return self.nlp.evaluate_constraints()

        def update_con():
            self.c = con_wrapped()

        self._update_con_impl = update_con
        self._update_con()

        # Jacobian evaluation
        def jac_wrapped():
            self.njev += 1
            return self.nlp.evaluate_jacobian().todense()
        
        def update_jac():
            self.J = jac_wrapped()

        self._update_jac_impl = update_jac
        self._update_jac()

        # Update x
        def update_x(x):
            self.x = x
            self.nlp.set_primals(x)
            for k, v in self.outervars.items():
                v.value = self.x[self.outervars_indices[k]]
            self.f_updated = False
            self.g_updated = False
            self.H_updated = False
            self.c_updated = False
            self.J_updated = False

        self._update_x_impl = update_x

        # Update duals
        def update_duals(duals):
            self.duals = duals
            self.nlp.set_duals(duals)
            self.H_updated = False

        self._update_duals_impl = update_duals

        # Update objective factor
        def update_obj_factor(obj_factor):
            self.obj_factor = obj_factor
            self.nlp.set_obj_factor(obj_factor)
            self.H_updated = False

        self._update_obj_factor_impl = update_obj_factor

    def _update_fun(self):
        if not self.f_updated:
            self._update_fun_impl()
            self.f_updated = True

    def _update_grad(self):
        if not self.g_updated:
            self._update_grad_impl()
            self.g_updated = True

    def _update_hess(self):
        if not self.H_updated:
            self._update_hess_impl()
            self.H_updated = True

    def _update_con(self):
        if not self.c_updated:
            self._update_con_impl()
            self.c_updated = True

    def _update_jac(self):
        if not self.J_updated:
            self._update_jac_impl()
            self.J_updated = True

    # wrap functions to evaluete only if x, duals and object_factor are updated
    def fun(self, x):
        if not np.array_equal(x, self.x):
            self._update_x_impl(x)
        self._update_fun()
        return self.f

    def grad(self, x):
        if not np.array_equal(x, self.x):
            self._update_x_impl(x)
        self._update_grad()
        return self.g

    def hess(self, x, duals, obj_factor):
        if not np.array_equal(x, self.x):
            self._update_x_impl(x)
        if not np.array_equal(duals, self.duals):
            self._update_duals_impl(duals) 
        if not np.array_equal(obj_factor, self.obj_factor):
            self._update_obj_factor_impl(obj_factor)
        self._update_hess()
        return self.H

    def con(self, x):
        if not np.array_equal(x, self.x):
            self._update_x_impl(x)
        self._update_con()
        # df_c = pd.DataFrame(self.c, index = self.nlp.constraint_names(), columns = ['body'])
        # df_c.to_csv('c_' + str(self.ncev) +'.csv', header = True, index = True)
        return self.c

    def jac(self, x):
        if not np.array_equal(x, self.x):
            self._update_x_impl(x)
        self._update_jac()
        # df_J = pd.DataFrame(self.J, index = self.nlp.constraint_names(), columns = [v for v in self.outervars.keys()])
        # df_J.to_csv('jac_' + str(self.njev) +'.csv', header = True, index = True)
        return self.J        
