from PyMPDATA import Solver, Stepper, Options, ScalarField, VectorField
from PyMPDATA.boundary_conditions import Extrapolated
from PySDM.impl import arakawa_c
import numpy as np


class MPDATA_1D:
    def __init__(
        self, nz, dt, advector_of_t, advectee_of_zZ_at_t0, g_factor_of_zZ, mpdata_settings
    ):
        self.t = 0
        self.dt = dt
        self.advector_of_t = advector_of_t

        grid = (nz,)
        options = Options(
            n_iters=mpdata_settings['n_iters'],
            infinite_gauge=mpdata_settings['iga'],
            nonoscillatory=mpdata_settings['fct'],
            third_order_terms=mpdata_settings['tot']
        )
        stepper = Stepper(options=options, grid=grid, non_unit_g_factor=True)
        bcs = (Extrapolated(),)
        g_factor = ScalarField(
            data=g_factor_of_zZ(arakawa_c.z_scalar_coord(grid)),
            halo=options.n_halo,
            boundary_conditions=bcs
        )
        advector = VectorField(
            data=(np.full(nz+1, advector_of_t(0)),),
            halo=options.n_halo,
            boundary_conditions=bcs
        )
        self.advectee = ScalarField(
            data=advectee_of_zZ_at_t0(arakawa_c.z_scalar_coord(grid)),
            halo=options.n_halo,
            boundary_conditions=bcs
        )
        self.solver = Solver(
            stepper=stepper,
            advectee=self.advectee,
            advector=advector,
            g_factor=g_factor
        )

    def __call__(self):
        self.t += .5 * self.dt
        self.solver.advector.get_component(0)[:] = self.advector_of_t(self.t)
        self.solver.advance(1)
        self.t += .5 * self.dt
