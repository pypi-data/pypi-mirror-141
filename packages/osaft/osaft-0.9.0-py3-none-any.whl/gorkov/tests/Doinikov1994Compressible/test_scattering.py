import unittest

import numpy as np

from gorkov.core.functions import SpecialFunctions as Sp
from gorkov.solutions.Doinikov1994Compressible.scattering import (
    ScatteringField,
)
from gorkov.tests.basetest import BaseTest
from gorkov.tests.basetest_scattering import HelperScattering


class TestScattering(HelperScattering, BaseTest):

    def setUp(self) -> None:
        super().setUp()

        self._v_particle_threshold = 1e-5
        self._v_fluid_threshold = 1e-3
        self._v_boundary_conditions = 1e-10

        self.cls = ScatteringField(
            self.f, self.R_0,
            self.rho_s, self.c_s,
            self.eta_p, self.zeta_p,
            self.rho_f, self.c_f,
            self.eta_f, self.zeta_f,
            self.p_0, self.wave_type,
            self.position,
        )

    # ------------------
    # fluid velocity
    # ------------------

    def V_r_sc(self, n, r) -> complex:
        # grad(phi)
        out = self.cls.k_f * self.alpha_n(n)
        out *= Sp.d1_hankelh1(n, self.cls.k_f * r)
        # curl(Psi)
        arg = self.cls.k_v * r
        out -= n * (n + 1) / r * self.beta_n(n) * Sp.hankelh1(n, arg)

        return out

    def V_theta_sc(self, n, r) -> complex:
        # curl(Psi)
        arg_v = self.cls.k_v * r
        out = Sp.hankelh1(n, arg_v)
        out += arg_v * Sp.d1_hankelh1(n, arg_v)
        out *= -self.beta_n(n)
        # grad(phi)
        out += self.alpha_n(n) * Sp.hankelh1(n, self.cls.k_f * r)

        out /= r
        return out

    # ------------------
    # particle velocity
    # ------------------

    def radial_particle_velocity(self, r, theta, t, mode):
        def vel(n, r):
            out = self.cls.k_s * self.alpha_hat_n(n)
            out *= Sp.d1_besselj(n, r * self.cls.k_s)

            arg = r * self.cls.k_vs
            out -= n * (n + 1) / r * self.beta_hat_n(n) * Sp.besselj(n, arg)
            return out

        out = self.cls.radial_mode_superposition(
            vel, r, theta, t, mode,
        )

        return out

    def tangential_particle_velocity(self, r, theta, t, mode):
        def vel(n, r):
            arg = r * self.cls.k_vs
            out = Sp.besselj(n, arg) + arg * Sp.d1_besselj(n, arg)
            out *= -self.beta_hat_n(n)

            out += self.alpha_hat_n(n) * Sp.besselj(n, r * self.cls.k_s)

            return out / r

        out = self.cls.tangential_mode_superposition(
            vel, r, theta, t, mode,
        )

        return out

    # ------------------
    # generic test method for coefficients
    # ------------------

    def test_coefficients(self) -> None:
        dict_of_methods = {}
        names = [
            'n_1', 'n_2', 'n_3', 'n_4',
            'm_11', 'm_12', 'm_13', 'm_14',
            'm_21', 'm_22', 'm_23', 'm_24',
            'm_31', 'm_32', 'm_33', 'm_34',
            'm_41', 'm_42', 'm_43', 'm_44',
            'det_M_n', 'det_M_1_n', 'det_M_2_n', 'det_M_3_n', 'det_M_4_n',
            'alpha_n', 'beta_n', 'alpha_hat_n', 'beta_hat_n',
        ]
        for name in names:
            dict_of_methods[name] = None

        self._test_methods_n(dict_of_methods, threshold=1e-8)

    # ------------------
    # testing scattering coefficients
    # ------------------

    def alpha_n(self, n: int) -> complex:
        return self.det_M_1_n(n) / self.det_M_n(n)

    def beta_n(self, n: int) -> complex:
        if n > 0:
            return self.det_M_2_n(n) / self.det_M_n(n)
        else:
            return 0

    def alpha_hat_n(self, n: int) -> complex:
        return self.det_M_3_n(n) / self.det_M_n(n)

    def beta_hat_n(self, n: int) -> complex:
        if n > 0:
            return self.det_M_4_n(n) / self.det_M_n(n)
        else:
            return 0

    # ------------------
    # testing determinants
    # ------------------

    def _get_matrix_from_list(self, coefficients: list, n: int) -> np.ndarray:
        out = np.zeros((4, 4), dtype=np.complex_)
        for i, name in enumerate(coefficients):
            col = i % 4
            row = i // 4
            #  print(name, i, row, col)
            out[row, col] = getattr(self, name)(n)

        return out

    def _get_M_matrix(self, n: int) -> np.ndarray:
        names = [
            'm_11', 'm_12', 'm_13', 'm_14',
            'm_21', 'm_22', 'm_23', 'm_24',
            'm_31', 'm_32', 'm_33', 'm_34',
            'm_41', 'm_42', 'm_43', 'm_44',
        ]

        return self._get_matrix_from_list(names, n)

    def _get_M_i_matrix(self, n: int, i: int) -> np.ndarray:
        M = self._get_M_matrix(n)
        for j in np.arange(4):
            M[j, i - 1] = getattr(self, f'n_{j+1:1.0f}')(n)
        return M

    def det_M_n(self, n: int) -> complex:
        return np.linalg.det(self._get_M_matrix(n))

    def det_M_1_n(self, n: int) -> complex:
        return np.linalg.det(self._get_M_i_matrix(n, 1))

    def det_M_2_n(self, n: int) -> complex:
        return np.linalg.det(self._get_M_i_matrix(n, 2))

    def det_M_3_n(self, n: int) -> complex:
        return np.linalg.det(self._get_M_i_matrix(n, 3))

    def det_M_4_n(self, n: int) -> complex:
        return np.linalg.det(self._get_M_i_matrix(n, 4))

    # ------------------
    # testing m_1i
    # ------------------

    def m_11(self, n: int) -> complex:
        out = self.x * Sp.d1_hankelh1(n, self.x)
        return out

    def m_12(self, n: int) -> complex:
        out = -n * (n + 1) * Sp.hankelh1(n, self.x_v)
        return out

    def m_13(self, n: int) -> complex:
        out = -self.x_hat * Sp.d1_besselj(n, self.x_hat)
        return out

    def m_14(self, n: int) -> complex:
        out = n * (n + 1) * Sp.besselj(n, self.x_hat_v)
        return out

    # ------------------
    # testing m_2i
    # ------------------

    def m_21(self, n: int) -> complex:
        out = Sp.hankelh1(n, self.x)
        return out

    def m_22(self, n: int) -> complex:
        out = -Sp.hankelh1(n, self.x_v)
        out -= self.x_v * Sp.d1_hankelh1(n, self.x_v)
        return out

    def m_23(self, n: int) -> complex:
        out = -Sp.besselj(n, self.x_hat)
        return out

    def m_24(self, n: int) -> complex:
        out = Sp.besselj(n, self.x_hat_v)
        out += self.x_hat_v * Sp.d1_besselj(n, self.x_hat_v)
        return out

    # ------------------
    # testing m_3i
    # ------------------

    def m_31(self, n: int) -> complex:
        out = 1j * self.cls.rho_f * self.cls.c_f**2 / self.cls.omega
        out += self.cls.zeta_f
        out -= 2 * self.cls.eta_f / 3
        out *= -Sp.hankelh1(n, self.x)

        out += 2 * self.cls.eta_f * Sp.d2_hankelh1(n, self.x)

        out *= self.x**2

        return out

    def m_32(self, n: int) -> complex:
        out = Sp.hankelh1(n, self.x_v)
        out -= self.x_v * Sp.d1_hankelh1(n, self.x_v)

        out *= 2 * n * (n + 1) * self.cls.eta_f
        return out

    def m_33(self, n: int) -> complex:
        out = 1j * self.cls.rho_s * self.cls.c_s**2 / self.cls.omega
        out += self.cls.zeta_p
        out -= 2 * self.cls.eta_p / 3
        out *= Sp.besselj(n, self.x_hat)

        out -= 2 * self.cls.eta_p * Sp.d2_besselj(n, self.x_hat)

        out *= self.x_hat**2
        return out

    def m_34(self, n: int) -> complex:
        out = -Sp.besselj(n, self.x_hat_v)
        out += self.x_hat_v * Sp.d1_besselj(n, self.x_hat_v)

        out *= 2 * n * (n + 1) * self.cls.eta_p
        return out

    # ------------------
    # testing m_4i
    # ------------------

    def m_41(self, n: int) -> complex:
        out = self.x * Sp.d1_hankelh1(n, self.x)
        out -= Sp.hankelh1(n, self.x)

        out *= 2 * self.cls.eta_f

        return out

    def m_42(self, n: int) -> complex:
        out = (n ** 2 + n - 2) * Sp.hankelh1(n, self.x_v)

        out += self.x_v**2 * Sp.d2_hankelh1(n, self.x_v)

        out *= -self.cls.eta_f
        return out

    def m_43(self, n: int) -> complex:
        out = Sp.besselj(n, self.x_hat)
        out -= self.x_hat * Sp.d1_besselj(n, self.x_hat)

        out *= 2 * self.cls.eta_p
        return out

    def m_44(self, n: int) -> complex:
        out = (n ** 2 + n - 2) * Sp.besselj(n, self.x_hat_v)

        out += self.x_hat_v**2 * Sp.d2_besselj(n, self.x_hat_v)

        out *= self.cls.eta_p
        return out

    # ------------------
    # testing n_i
    # ------------------

    def n_1(self, n: int) -> complex:
        out = -self.x * Sp.d1_besselj(n, self.x)
        out *= self.cls.A_in(n)
        return out

    def n_2(self, n: int) -> complex:
        out = -Sp.besselj(n, self.x)
        out *= self.cls.A_in(n)
        return out

    def n_3(self, n: int) -> complex:
        out = 1j * self.cls.rho_f * self.cls.c_f**2 / self.cls.omega
        out += self.cls.zeta_f
        out -= 2 * self.cls.eta_f / 3
        out *= Sp.besselj(n, self.x)

        out -= 2 * self.cls.eta_f * Sp.d2_besselj(n, self.x)

        out *= self.x ** 2 * self.cls.A_in(n)

        return out

    def n_4(self, n: int) -> complex:
        out = Sp.besselj(n, self.x)
        out -= self.x * Sp.d1_besselj(n, self.x)

        out *= 2 * self.cls.eta_f * self.cls.A_in(n)
        return out

    # ------------------
    @property
    def x(self):
        return self.cls.x

    @property
    def x_v(self):
        return self.cls.x_v

    @property
    def x_hat(self):
        return self._compute_x_hat()

    def _compute_x_hat(self) -> complex:
        return self.R_0 * self.cls.k_s

    def test_x(self) -> None:
        self.do_testing(
            func_1=self._compute_x_hat,
            func_2=lambda: self.cls.x_hat,
        )

    # ------------------

    @property
    def x_hat_v(self):
        return self._compute_x_hat_v()

    def _compute_x_hat_v(self) -> complex:
        return self.R_0 * self.cls.k_vs

    def test_x_hat_v(self) -> None:
        self.do_testing(
            func_1=self._compute_x_hat_v,
            func_2=lambda: self.cls.x_hat_v,
        )


if __name__ == '__main__':
    unittest.main()
