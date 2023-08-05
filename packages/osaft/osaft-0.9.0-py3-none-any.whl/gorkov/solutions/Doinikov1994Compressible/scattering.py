from typing import Optional, Union

import numpy as np

from gorkov import log
from gorkov.core.backgroundfields import WaveTypes
from gorkov.core.frequency import Frequency
from gorkov.core.functions import SpecialFunctions as Sp
from gorkov.core.functions import full_range
from gorkov.core.geometries import Sphere
from gorkov.core.helper import InputHandler
from gorkov.core.variable import ActiveVariable
from gorkov.solutions.base_scattering import BaseScattering
from gorkov.solutions.Doinikov1994Compressible.base import (
    BaseDoinikov1994Compressible,
)
from gorkov.solutions.Doinikov1994Compressible.coefficientmatrix import (
    CoefficientMatrix,
)


class ScatteringField(
    CoefficientMatrix,
    BaseDoinikov1994Compressible,
    BaseScattering,
):
    """Scattering field of Doinikov (viscous fluid-viscous sphere; 1994)

    :param frequency: Frequency [Hz]
    :param radius: Radius of the solid [m]
    :param rho_s: Density of the fluid-like solid [kg/m^3]
    :param c_s: Speed of sound of the sphere [m/s]
    :param eta_p: shear viscosity of the sphere [Pa s]
    :param zeta_p: bulk viscosity of the sphere [Pa s]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity [Pa s]
    :param zeta_f: bulk viscosity [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param position: Position within the standing wave field [m]
    :param wave_type: Type of wave, travel(l)ing or standing
    :param N_max: Highest order mode
    """

    def __init__(
        self, frequency: Union[Frequency, float, int],
        radius: Union[Sphere, float, int],
        rho_s: float, c_s: float, eta_p: float, zeta_p: float,
        rho_f: float, c_f: float, eta_f: float, zeta_f: float,
        p_0: float,
        wave_type: WaveTypes = WaveTypes.STANDING,
        position: Optional[float] = None,
        N_max: Optional[int] = 5,
    ) -> None:
        """Constructor method
        """

        # init of parent class
        CoefficientMatrix.__init__(self)
        BaseDoinikov1994Compressible.__init__(
            self, frequency, radius,
            rho_s, c_s, eta_p, zeta_p,
            rho_f, c_f, eta_f, zeta_f,
            p_0, wave_type, position, N_max,
        )

        self._create_variables()
        self._set_links()

        if type(self) is ScatteringField:
            log.debug(repr(self))
            log.info(str(self))

    def _create_variables(self) -> None:
        # Dependent variables
        self._det_M_n = ActiveVariable(
            self._reset_list,
            'determinant of M matrix',
        )
        self._det_M_1_n = ActiveVariable(
            self._reset_list,
            'determinant of M_1 matrix',
        )
        self._det_M_2_n = ActiveVariable(
            self._reset_list,
            'determinant of M_2 matrix',
        )
        self._det_M_3_n = ActiveVariable(
            self._reset_list,
            'determinant of M_3 matrix',
        )
        self._det_M_4_n = ActiveVariable(
            self._reset_list,
            'determinant of M_4 matrix',
        )

        self._alpha_n = ActiveVariable(
            self._reset_list,
            'fluid scattering coefficient alpha_n',
        )

        self._beta_n = ActiveVariable(
            self._reset_list,
            'fluid scattering coefficient beta_n',
        )

        self._alpha_hat_n = ActiveVariable(
            self._reset_list, 'sphere scattering coefficient alpha_hat_n',
        )

        self._beta_hat_n = ActiveVariable(
            self._reset_list, 'sphere scattering coefficient beta_hat_n',
        )

        self._x = ActiveVariable(self._compute_x)
        self._x_v = ActiveVariable(self._compute_x_v)

        self._x_hat = ActiveVariable(self._compute_x_hat)
        self._x_hat_v = ActiveVariable(self._compute_x_hat_v)

    def _set_links(self) -> None:
        # define dependencies
        self._x.is_computed_by(
            self.fluid._k_f, self.sphere._R_0,
        )
        self._x_v.is_computed_by(
            self.fluid._k_v, self.sphere._R_0,
        )

        self._x_hat.is_computed_by(
            self.solid._k_f, self.sphere._R_0,
        )
        self._x_hat_v.is_computed_by(
            self.solid._k_v, self.sphere._R_0,
        )

        # determinants
        self._det_M_n.is_computed_by(
            #  self._n,
            self._m_11, self._m_12, self._m_13, self._m_14,
            self._m_21, self._m_22, self._m_23, self._m_24,
            self._m_31, self._m_32, self._m_33, self._m_34,
            self._m_41, self._m_42, self._m_43, self._m_44,
        )

        self._det_M_1_n.is_computed_by(
            #  self._n,
            self._m_21, self._m_22, self._m_23, self._m_24,
            self._m_31, self._m_32, self._m_33, self._m_34,
            self._m_41, self._m_42, self._m_43, self._m_44,
            self._n_1, self._n_2, self._n_3, self._n_4,
        )

        self._det_M_2_n.is_computed_by(
            #  self._n,
            self._m_11, self._m_12, self._m_13, self._m_14,
            self._n_1, self._n_2, self._n_3, self._n_4,
            self._m_31, self._m_32, self._m_33, self._m_34,
            self._m_41, self._m_42, self._m_43, self._m_44,
        )

        self._det_M_3_n.is_computed_by(
            #  self._n,
            self._m_11, self._m_12, self._m_13, self._m_14,
            self._m_21, self._m_22, self._m_23, self._m_24,
            self._n_1, self._n_2, self._n_3, self._n_4,
            self._m_41, self._m_42, self._m_43, self._m_44,
        )
        self._det_M_4_n.is_computed_by(
            #  self._n,
            self._m_11, self._m_12, self._m_13, self._m_14,
            self._m_21, self._m_22, self._m_23, self._m_24,
            self._m_31, self._m_32, self._m_33, self._m_34,
            self._n_1, self._n_2, self._n_3, self._n_4,
        )

        # RHS vector
        self._n_1.is_computed_by(self._x)
        self._n_2.is_computed_by(self._x)
        self._n_3.is_computed_by(
            self._x, self.frequency._omega,
            self.fluid._eta_f,
            self.fluid._zeta_f,
        )
        self._n_4.is_computed_by(self._x, self.fluid._eta_f)

        # matrix entries m_1j
        self._m_11.is_computed_by(self._x)
        self._m_12.is_computed_by(self._x_v)
        self._m_13.is_computed_by(self._x_hat)
        self._m_14.is_computed_by(self._x_hat_v)

        # matrix entries m_2j
        self._m_21.is_computed_by(self._x)
        self._m_22.is_computed_by(self._x_v)
        self._m_23.is_computed_by(self._x_hat)
        self._m_24.is_computed_by(self._x_hat_v)

        # matrix entries m_3j
        self._m_31.is_computed_by(
            self._x, self.fluid._eta_f, self.fluid._zeta_f, self.fluid._rho_f,
            self.fluid._c_f, self.frequency._omega,
        )
        self._m_32.is_computed_by(self._x_v, self.fluid._eta_f)
        self._m_33.is_computed_by(
            self._x_hat, self.solid._eta_f, self.solid._zeta_f,
            self.solid._rho_f, self.solid._c_f, self.frequency._omega,
        )
        self._m_34.is_computed_by(self._x_hat_v, self.solid._eta_f)

        # matrix entries m_3j
        self._m_41.is_computed_by(self._x, self.fluid._eta_f)
        self._m_42.is_computed_by(self._x_v, self.fluid._eta_f)
        self._m_43.is_computed_by(self._x_hat, self.solid._eta_f)
        self._m_44.is_computed_by(self._x_hat_v, self.solid._eta_f)

    def __repr__(self):
        return (
            f'Doinikov1994Compressible.ScatteringFiels(frequency={self.f}, '
            f'radius={self.R_0}, '
            f'rho_s={self.rho_s}, c_s={self.c_s}, '
            f'eta_p={self.eta_p}, zeta_p={self.zeta_p}, '
            f'rho_f={self.rho_f}, c_f={self.c_f}, '
            f'eta_f={self.eta_f}, zeta_f={self.zeta_f}, '
            f'p_0={self.p_0}, position={self.position}, {self.wave_type}, '
            f'N_max={self.N_max})'
        )
    # -----------------------------------------------------
    # Determinants of matrices
    # -----------------------------------------------------

    def det_M_n(self, n: int) -> complex:
        """Determinant of M matrix of order n

        :param n: order
        """
        if n < len(self._det_M_n.value):
            return self._det_M_n.value[n]
        else:
            self._compute_det_M_n(n)
            return self._det_M_n.value[n]

    def _compute_det_M_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._det_M_n.value)
        for n in full_range(N_old, N):
            self._det_M_n.value.append(self.det_M(n))

    def det_M_1_n(self, n: int) -> complex:
        """Determinant of M_1 matrix of order n

        :param n: order
        """
        if n < len(self._det_M_1_n.value):
            return self._det_M_1_n.value[n]
        else:
            self._compute_det_M_1_n(n)
            return self._det_M_1_n.value[n]

    def _compute_det_M_1_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._det_M_1_n.value)
        for n in full_range(N_old, N):
            self._det_M_1_n.value.append(self.det_M_1(n))

    def det_M_2_n(self, n: int) -> complex:
        """Determinant of M_2 matrix of order n

        :param n: order
        """
        if n < len(self._det_M_2_n.value):
            return self._det_M_2_n.value[n]
        else:
            self._compute_det_M_2_n(n)
            return self._det_M_2_n.value[n]

    def _compute_det_M_2_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._det_M_2_n.value)
        for n in full_range(N_old, N):
            self._det_M_2_n.value.append(self.det_M_2(n))

    def det_M_3_n(self, n: int) -> complex:
        """Determinant of M_3 matrix of order n

        :param n: order
        """
        if n < len(self._det_M_3_n.value):
            return self._det_M_3_n.value[n]
        else:
            self._compute_det_M_3_n(n)
            return self._det_M_3_n.value[n]

    def _compute_det_M_3_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._det_M_3_n.value)
        for n in full_range(N_old, N):
            self._det_M_3_n.value.append(self.det_M_3(n))

    def det_M_4_n(self, n: int) -> complex:
        """Determinant of M_4 matrix of order n

        :param n: order
        """
        if n < len(self._det_M_4_n.value):
            return self._det_M_4_n.value[n]
        else:
            self._compute_det_M_4_n(n)
            return self._det_M_4_n.value[n]

    def _compute_det_M_4_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._det_M_4_n.value)
        for n in full_range(N_old, N):
            self._det_M_4_n.value.append(self.det_M_4(n))

    # -----------------------------------------------------
    # Scattering coefficients Fluid
    # -----------------------------------------------------

    def alpha_n(self, n: int) -> complex:
        """ coefficient :math:`\\alpha_n` (3.13) and (3.20)

        :param n: order
        """
        if n < len(self._alpha_n.value):
            return self._alpha_n.value[n]
        else:
            self._compute_alpha_n(n)
            return self._alpha_n.value[n]

    def _compute_alpha_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._alpha_n.value)
        for n in full_range(N_old, N):
            if n == 0:
                tmp1 = 4 * (self.eta_f - self.eta_p) * self.x * self.x_hat
                tmp1 *= Sp.besselj(1, self.x_hat)

                tmp2 = 1j * self.omega * self.R_0**2

                # numerator
                num = self.rho_f * self.x_hat
                num *= Sp.besselj(0, self.x) * Sp.besselj(1, self.x_hat)

                num -= self.rho_s * self.x * (
                    Sp.besselj(1, self.x) *
                    Sp.besselj(0, self.x_hat)
                )

                num *= tmp2

                num -= tmp1 * Sp.besselj(1, self.x)

                # denominator
                den = self.rho_s * self.x
                den *= Sp.hankelh1(1, self.x) * Sp.besselj(0, self.x_hat)

                den -= self.rho_f * self.x_hat * (
                    Sp.hankelh1(0, self.x) *
                    Sp.besselj(1, self.x_hat)
                )

                den *= tmp2

                den += tmp1 * Sp.hankelh1(1, self.x)

                new_value = num / den * self.A_in(0)
            else:
                new_value = self.det_M_1_n(n) / self.det_M_n(n)

            self._alpha_n.value.append(new_value)

    def beta_n(self, n: int) -> complex:
        """ coefficient :math:`\\beta_n` (3.13) and (3.20)

        :param n: order
        """
        if n < len(self._beta_n.value):
            return self._beta_n.value[n]
        else:
            self._compute_beta_n(n)
            return self._beta_n.value[n]

    def _compute_beta_n(self, N: int) -> None:
        # computation according to (3.13), (3.15) and (3.21)

        N_old = len(self._beta_n.value)
        for n in full_range(N_old, N):
            if n == 0:
                new_value = 0.0
            else:
                new_value = self.det_M_2_n(n) / self.det_M_n(n)

            self._beta_n.value.append(new_value)

    # -----------------------------------------------------
    # Scattering coefficients sphere
    # -----------------------------------------------------

    def alpha_hat_n(self, n: int) -> complex:
        """ coefficient :math:`\\alpha_hat_n` (3.13) and (3.20)

        :param n: order
        """
        if n < len(self._alpha_hat_n.value):
            return self._alpha_hat_n.value[n]
        else:
            self._compute_alpha_hat_n(n)
            return self._alpha_hat_n.value[n]

    def _compute_alpha_hat_n(self, N: int) -> None:
        # computation according to (3.13), (3.14) and (3.20)

        N_old = len(self._alpha_hat_n.value)
        for n in full_range(N_old, N):
            if n == 0:
                tmp1 = 4 * (self.eta_f - self.eta_p) * self.x * self.x_hat
                tmp2 = 1j * self.omega * self.R_0**2

                # numerator
                num = Sp.besselj(0, self.x) * Sp.hankelh1(1, self.x)

                num -= Sp.besselj(1, self.x) * Sp.hankelh1(0, self.x)

                num *= tmp2 * self.x * self.rho_f

                # denominator
                den = self.rho_s * self.x
                den *= Sp.hankelh1(1, self.x) * Sp.besselj(0, self.x_hat)

                den -= self.rho_f * self.x_hat * (
                    Sp.hankelh1(0, self.x) *
                    Sp.besselj(1, self.x_hat)
                )

                den *= tmp2

                den += tmp1 * (
                    Sp.hankelh1(1, self.x) *
                    Sp.besselj(1, self.x_hat)
                )

                new_value = num / den * self.A_in(0)
            else:
                new_value = self.det_M_3_n(n) / self.det_M_n(n)

            self._alpha_hat_n.value.append(new_value)

    def beta_hat_n(self, n: int) -> complex:
        """ coefficient :math:`\\beta_hat_n` (3.13) and (3.20)

        :param n: order
        """
        if n < len(self._beta_hat_n.value):
            return self._beta_hat_n.value[n]
        else:
            self._compute_beta_hat_n(n)
            return self._beta_hat_n.value[n]

    def _compute_beta_hat_n(self, N: int) -> None:
        # computation according to (3.13), (3.15) and (3.21)

        N_old = len(self._beta_hat_n.value)
        for n in full_range(N_old, N):
            if n == 0:
                new_value = 0.0
            else:
                new_value = self.det_M_4_n(n) / self.det_M_n(n)

            self._beta_hat_n.value.append(new_value)

    # -----------------------------------------------------
    # Scattering coefficients sphere
    # -----------------------------------------------------

    @staticmethod
    def _reset_list() -> list:
        return []

    @property
    def x(self) -> complex:
        """Product of :attr:`~.k_f` and :attr:`~.R_0`
        """
        return self._x.value

    def _compute_x(self) -> complex:
        return self.k_f * self.R_0

    @property
    def x_v(self) -> complex:
        """Product of :attr:`~.k_v` and :attr:`~.R_0`
        """
        return self._x_v.value

    def _compute_x_v(self) -> complex:
        return self.k_v * self.R_0

    @property
    def x_hat(self) -> complex:
        """Product of :attr:`~.k_f` and :attr:`~.R_0`
        """
        return self._x_hat.value

    def _compute_x_hat(self) -> complex:
        return self.k_s * self.R_0

    @property
    def x_hat_v(self) -> complex:
        """Product of :attr:`~.k_v` and :attr:`~.R_0`
        """
        return self._x_hat_v.value

    def _compute_x_hat_v(self) -> complex:
        return self.k_vs * self.R_0

    # -----------------------------------------------------
    # Methods
    # -----------------------------------------------------

    def V_r_sc(self, n: int, r: float) -> complex:
        """Radial scattering field velocity term of mode `n`
        without Legendre coefficients

        Returns radial scattering field velocity in [m/s]

        :param n: mode
        :param r: radial coordinate [m]
        """
        out = self.k_f * self.alpha_n(n) * Sp.d1_hankelh1(n, r * self.k_f)
        out -= n * (n + 1) / r * self.beta_n(n) * Sp.hankelh1(n, r * self.k_v)
        #  out *= self.A_in(n)
        return out

    def V_theta_sc(self, n: int, r: float) -> complex:
        """ Tangential scattering field velocity term of mode n
        without Legendre coefficients

        Returns tangential scattering field velocity in [m/s]

        :param n: mode
        :param r: radial coordinate [m]
        """

        arg = self.k_v * r
        out = Sp.hankelh1(n, arg)
        out += arg * Sp.d1_hankelh1(n, arg)
        out *= -self.beta_n(n)

        out += self.alpha_n(n) * Sp.hankelh1(n, self.k_f * r)

        #  out *= self.A_in(n)

        return out / r

    def radial_particle_velocity(
        self,
        r: Union[float, np.ndarray, list[float]],
        theta: Union[float, np.ndarray, list[float]],
        t: Union[float, np.ndarray, list[float]],
        mode: Optional[int] = None,
    ) -> float:
        """Particle velocity in radial direction

        Returns the value of the particle velocity
        in radial direction in [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific modenumber of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        r, theta, t = InputHandler.handle_input(
            r, theta, t, self.R_0,
            inside_sphere=True,
        )

        def radial_velocity(n: int, r: float) -> complex:
            out = self.k_s * self.alpha_hat_n(n)
            out *= Sp.d1_besselj(n, r * self.k_s)

            arg = r * self.k_vs
            out -= n * (n + 1) / r * self.beta_hat_n(n) * Sp.besselj(n, arg)

            return out

        out = self.radial_mode_superposition(
            radial_velocity, r, theta, t, mode,
        )

        return out

    def tangential_particle_velocity(
            self,
            r: Union[float, np.ndarray, list[float]],
            theta: Union[float, np.ndarray, list[float]],
            t: Union[float, np.ndarray, list[float]],
            mode: Optional[int] = None,
    ) -> float:
        """Particle velocity in tangential direction

        Returns the value of the particle velocity
        in tangential direction in [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific modenumber of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        r, theta, t = InputHandler.handle_input(
            r, theta, t, self.R_0,
            inside_sphere=True,
        )

        def tangential_velocity(n: int, r: float) -> complex:
            out = Sp.besselj(n, self.k_vs * r)
            out += r * self.k_vs * Sp.d1_besselj(n, self.k_vs * r)
            out *= -self.beta_hat_n(n)

            out += self.alpha_hat_n(n) * Sp.besselj(n, self.k_s * r)

            return out / r

        out = self.tangential_mode_superposition(
            tangential_velocity, r, theta, t, mode,
        )

        return out


if __name__ == '__main__':
    pass
