from __future__ import annotations

from typing import Optional, Union

from gorkov import log
from gorkov.core.backgroundfields import WaveTypes, WrongWaveTypeError
from gorkov.core.basecomposite import BaseSphereFrequencyComposite
from gorkov.core.frequency import Frequency
from gorkov.core.functions import pi, sin, sqrt
from gorkov.core.geometries import Sphere
from gorkov.core.helper import StringFormatter as SF
from gorkov.core.variable import ActiveVariable, PassiveVariable
from gorkov.solutions.base_arf import BaseARF
from gorkov.solutions.Doinikov1994Compressible.scattering import (
    ScatteringField,
)


class ARF(ScatteringField, BaseARF, BaseSphereFrequencyComposite):
    """Base class for Doinikov (viscous fluid-viscous sphere; 1994)

    .. note::
       For all models the condition :math:`|x| \\ll 1` must hold.

       If :attr:`small_viscous_boundary_layer` is set to `True` than in
       addition :math:`|x| \\ll |x_v| \\ll 1` must hold. If set to
       `False` than :math:`|x| \\ll 1 \\ll |x_v|` must hold.

       Both values will be logged in the `info.log` when calling
       :meth:`acoustic_radiation_force`. These conditions will not be
       checked at runtime.


    :param frequency: Frequency [Hz]
    :param radius: Radius of the solid [m]
    :param rho_s: Density of the fluid-like solid [kg/m^3]
    :param c_s: Speed of sound of the solid [m/s]
    :param eta_p: shear viscosity of the solid [Pa s]
    :param zeta_p: bulk viscosity of the solid [Pa s]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity fluid [Pa s]
    :param zeta_f: bulk viscosity fluid [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param wave_type: Type of wave, travel(l)ing or standing
    :param position: Position within the standing wave field [m]
    :param small_viscous_boundary_layer: :math:`x_v \\ll 1`
    :param gas_bubble: solid is a gas bubble in a liquid
    :param small_particle_limit: using the limiting cases for the ARF
    :param N_max: Highest order mode
    """

    def __init__(
        self, frequency: Union[Frequency, float, int],
        radius: Union[Sphere, float, int],
        rho_s: float, c_s: float,
        eta_p: float, zeta_p: float,
        rho_f: float, c_f: float,
        eta_f: float, zeta_f: float,
        p_0: float,
        wave_type: WaveTypes = WaveTypes.STANDING,
        position: Optional[float] = None,
        small_viscous_boundary_layer: bool = True,
        gas_bubble: bool = False,
        small_particle_limit: bool = True,
        N_max: int = 5,
    ) -> None:
        """Constructor method
        """

        # init of parent class
        BaseSphereFrequencyComposite.__init__(self, frequency, radius)
        ScatteringField.__init__(
            self, frequency, radius,
            rho_s, c_s, eta_p, zeta_p,
            rho_f, c_f, eta_f, zeta_f,
            p_0, wave_type, position, N_max,
        )

        # independent variables
        self._check_small_particle_limit_value(small_particle_limit)
        self._small_particle_limit = PassiveVariable(
            small_particle_limit,
            'small particle limit',
        )
        self._small_viscous_boundary_layer = PassiveVariable(
            small_viscous_boundary_layer,
            'small viscous boundary layer limit',
        )

        self._check_gas_bubble(gas_bubble)
        self._gas_bubble = PassiveVariable(
            gas_bubble,
            'particle is a gas bubble',
        )

        # dependen variables
        self._norm_delta = ActiveVariable(
            self._compute_norm_delta,
            'normalized boundary layer thickness',
        )

        self._mu = ActiveVariable(
            self._compute_mu,
            '(density * viscosity) ratio',
        )

        self._kappa_t = ActiveVariable(
            self._compute_kappa_t,
            'compressibility ratio',
        )

        self._eta_t = ActiveVariable(
            self._compute_eta_t,
            'dynamic viscosity ratio',
        )

        self._zeta_t = ActiveVariable(
            self._compute_zeta_t,
            'bulk viscosity ratio',
        )

        self._f1 = ActiveVariable(
            self._compute_f1,
            'f1 ARF factor; B.2.1',
        )

        self._f2 = ActiveVariable(
            self._compute_f2,
            'f2 ARF factor; B.2.1',
        )

        self._f3 = ActiveVariable(
            self._compute_f3,
            'f3 ARF factor; B.2.1',
        )

        self._G = ActiveVariable(
            self._compute_G,
            'G ARF factor; eq. 7.9',
        )

        self._S1 = ActiveVariable(
            self._compute_S1,
            'S1 ARF factor; eq. 7.10',
        )

        self._S2 = ActiveVariable(
            self._compute_S2,
            'S2 ARF factor; eq. 7.11',
        )

        self._S3 = ActiveVariable(
            self._compute_S3,
            'S3 ARF factor; eq. 7.12',
        )

        self._f4 = ActiveVariable(
            self._compute_f4,
            'f4 ARF factor; B.2.1',
        )

        self._g1 = ActiveVariable(
            self._compute_g1,
            'g1 ARF factor; B.2.1',
        )

        self._g2 = ActiveVariable(
            self._compute_g2,
            'g2 ARF factor; B.2.1',
        )

        self._g3 = ActiveVariable(
            self._compute_g3,
            'g3 ARF factor; B.2.1',
        )

        self._g4 = ActiveVariable(
            self._compute_g4,
            'g4 ARF factor; B.2.1',
        )

        self._g5 = ActiveVariable(
            self._compute_g5,
            'g5 ARF factor; B.2.1',
        )

        self._g6 = ActiveVariable(
            self._compute_g6,
            'g6 ARF factor; B.2.1',
        )

        self._g7 = ActiveVariable(
            self._compute_g7,
            'g7 ARF factor; B.2.1',
        )

        self._G.is_computed_by(self._S1, self._S2, self._S3)
        self._S1.is_computed_by(
            self._kappa_t,
            self.fluid._rho_f, self.solid._rho_f,
        )
        self._S2.is_computed_by(self._f1, self._f2, self._f4)
        self._S3.is_computed_by(
            self._f1, self._f3, self._f4,
            self.fluid._rho_f, self.solid._rho_f,
            self._kappa_t, self._eta_t,
        )

        self._eta_t.is_computed_by(self.solid._eta_f, self.fluid._eta_f)
        self._zeta_t.is_computed_by(self.solid._zeta_f, self.fluid._zeta_f)
        self._f1.is_computed_by(self._g1, self._g7)
        self._f2.is_computed_by(self._g1, self._g2, self._g5)
        self._f3.is_computed_by(self._g3, self._g6, self._g7)
        self._f4.is_computed_by(self._g4, self._g6, self._g7)
        self._g1.is_computed_by(self._g5, self._g6)
        self._g2.is_computed_by(self._eta_t, self._zeta_t)
        self._g3.is_computed_by(self._eta_t, self._zeta_t)
        self._g4.is_computed_by(self._eta_t, self._zeta_t)
        self._g5.is_computed_by(self._eta_t)
        self._g6.is_computed_by(self._eta_t)
        self._g7.is_computed_by(self._g6)

        self._norm_delta.is_computed_by(
            self.fluid._delta, self.sphere._R_0,
        )

        self._kappa_t.is_computed_by(
            self.fluid._rho_f, self.fluid._c_f,
            self.solid._rho_f, self.solid._c_f,
        )

        self._mu.is_computed_by(
            self.fluid._rho_f, self.fluid._eta_f,
            self.solid._rho_f, self.solid._eta_f,
        )

        # logging
        log.debug(repr(self))
        log.info(str(self))

    def __repr__(self):
        return (
            f'Donikov1994Rigid.ARF(frequency={self.f}, radius={self.R_0}, '
            f'rho_s={self.rho_s}, c_s={self.c_s}, '
            f'eta_p={self.eta_p}, zeta_p={self.zeta_p}, '
            f'rho_f={self.rho_f}, c_f={self.c_f}, '
            f'eta_f={self.eta_f}, zeta_f={self.zeta_f}, '
            f'p_0={self.p_0}, position={self.position}, {self.wave_type}, '
            f'small_viscous_boundary_layer='
            f'{self.small_viscous_boundary_layer}, '
            f'gas_bubble={self.gas_bubble}, '
            f'small_particle_limit={self.small_particle_limit}, '
            f'N_max={self.N_max})'
        )

    def __str__(self):
        out = 'Doinikovs\'s  (1994) model (viscous fluid-rigid sphere) for the'
        out += ' ARF with the following properties: \n'
        out += 'Limit Cases\n'
        out += SF.get_str_text(
            'Small particle limit',
            'small_particle_limit',
            self.small_particle_limit, None,
        )
        out += SF.get_str_text(
            'Small delta',
            'small_viscous_boundary_layer',
            self.small_viscous_boundary_layer, None,
        )
        out += SF.get_str_text(
            'Gas bubble',
            'gas_bubble',
            self.gas_bubble, None,
        )
        out += 'Backgroundfield\n'
        out += SF.get_str_text('Frequency', 'f', self.f, 'Hz')
        out += SF.get_str_text('Pressure', 'p_0', self.p_0, 'Pa')
        out += SF.get_str_text('Wavetype', 'wave_type', self.wave_type, None)
        out += SF.get_str_text(
            'Position', 'd',
            self.position, 'Pa',
        )
        out += SF.get_str_text(
            'Wavelength', 'lambda',
            self.field.lambda_f, 'm',
        )

        out += 'Fluid\n'
        out += SF.get_str_text(
            'Density', 'rho_f',
            self.rho_f, 'kg/m^3',
        )
        out += SF.get_str_text(
            'Sound Speed', 'c_0',
            self.c_f, 'm/s',
        )
        out += SF.get_str_text(
            'Compressibility', 'kappa_f',
            self.kappa_f, '1/Pa',
        )
        out += SF.get_str_text(
            'Shear viscosity', 'eta_f',
            self.eta_f, '1/Pa',
        )
        out += SF.get_str_text(
            'Bulk viscosity', 'zeta_f',
            self.zeta_f, '1/Pa',
        )

        out += 'Particle\n'
        out += SF.get_str_text(
            'Radius', 'R_0',
            self.R_0, 'm',
        )
        out += SF.get_str_text(
            'Density', 'rho_s',
            self.rho_s, 'kg/m^3',
        )
        out += SF.get_str_text(
            'Sound Speed', 'c_0',
            self.c_s, 'm/s',
        )
        out += SF.get_str_text(
            'Compressibility', 'kappa_s',
            self.kappa_s, '1/Pa',
        )
        out += SF.get_str_text(
            'Shear viscosity', 'eta_p',
            self.eta_p, '1/Pa',
        )
        out += SF.get_str_text(
            'Bulk viscosity', 'zeta_p',
            self.zeta_p, '1/Pa',
        )
        return out

    def acoustic_radiation_force(self) -> float:
        """Acoustic radiation fore in [N]

        It logs the current values of :attr:`x` and :attr:`x_v`.

        :raises ValueError: Non supported :attr:`~gorkov.solutions.\
Doinikov1994Rigid.baseclass.aseDoinikov1994Rigid.wave_type`
        """
        if not isinstance(self.wave_type, WaveTypes):
            raise WrongWaveTypeError

        # we do not need to test for gas_bubble yet because this solution right
        # now not permitted
        if self.small_viscous_boundary_layer:
            return self._liquid_in_liquid_small_delta()
        else:
            return self._liquid_in_liquid()

    def _liquid_in_liquid_small_delta(self) -> float:
        """ Eq. 7.1 for WaveTypes.TRAVELLING; Eq. 7.8 for WaveTypes.STANDING
        """
        log.info(
            f'kappa_t << 1 : {self.kappa_t:.3e} << 1\n'
            f'rho_f << rho_s : {self.rho_s:.3e} << {self.rho_s:.3e}\n',
        )

        if self.wave_type == WaveTypes.TRAVELLING:
            out = 5 - 2 * self.kappa_t - 8 * self._f1.value

            out *= 1 / 6 * self.norm_delta ** 2
        else:
            out = self._G.value * self._standing_wave_contribution()

        out *= pi * self.field.abs_A_squared * self.rho_f * self.x_0**3
        return out

    def _liquid_in_liquid(self) -> float:
        """ Eq. 6.1 for WaveTypes.TRAVELLING
        """
        log.info(
            f'kappa_t << 1 : {self.kappa_t:.3e} << 1\n'
            f'mu << 1 : {self.mu:.3e} << 1\n',
        )
        if self.wave_type == WaveTypes.TRAVELLING:
            out = (self.rho_s - self.rho_f) ** 2
            out /= (2 * self.rho_s + self.rho_f)**2 * (1 + self.mu)

            out *= self.x_0**3 * self.norm_delta

            out *= 6 * pi * self.rho_f * self.field.abs_A_squared
        else:
            raise NotImplementedError(
                'This solution is not implemented because Doinikov says '
                'in 6.1.2 of the publication that this solution is '
                'the same as Yosioka already computed.\n If you are '
                'interested in this value us the Yosioka class.',
            )

        return out

    def _standing_wave_contribution(self) -> float:
        return sin(2 * self.k_f.real * self.position)

    @staticmethod
    def _check_gas_bubble(value):
        if value:
            raise NotImplementedError(
                'You are trying to use the limiting case of a gas bubble '
                'for this model. However, so far this limiting case is not '
                'implemented. Feel free to help us to extend this.',
            )

    @staticmethod
    def _check_small_particle_limit_value(value):
        if not value:
            raise NotImplementedError(
                'You are trying to use the general solution to the ARF '
                'for this model. However, so far just the limiting cases '
                'are implemented. Feel free to help us to extend this.',
            )

    @property
    def small_particle_limit(self) -> bool:
        """Use limiting case for ARF calculation

        :getter: returns if a small particle limit is used
        :setter: automatically invokes
            :meth:`gorkov.core.variable.BaseVariable.notify`
        :raises NotImplementedError: If value is set to False; because just the
            limiting cases for the ARF are implemented
        """
        return self._small_particle_limit.value

    @small_particle_limit.setter
    def small_particle_limit(self, value):
        self._check_small_particle_limit_value(value)
        self._small_particle_limit.value = value

    @property
    def gas_bubble(self) -> bool:
        """Use limiting case of a gas bubble as solid

        :getter: returns if solid is a gas bubble
        :setter: automatically invokes
            :meth:`gorkov.core.variable.BaseVariable.notify`
        """
        return self._gas_bubble.value

    @gas_bubble.setter
    def gas_bubble(self, value):
        self._check_gas_bubble(value)
        self._gas_bubble.value = value

    @property
    def small_viscous_boundary_layer(self) -> bool:
        """Use limiting case of a small viscous boundary layer :math:`\\delta`

        :getter: returns if a small viscous boundary layer case is used
        :setter: automatically invokes
            :meth:`gorkov.core.variable.BaseVariable.notify`
        """
        return self._small_viscous_boundary_layer.value

    @small_viscous_boundary_layer.setter
    def small_viscous_boundary_layer(self, value):
        self._small_viscous_boundary_layer.value = value

    def _compute_eta_t(self):
        return self.solid.eta_f / self.fluid.eta_f

    def _compute_zeta_t(self):
        return self.solid.zeta_f / self.fluid.zeta_f

    def _compute_G(self):
        return (self._S1.value + self._S2.value + self._S3.value) / 3

    def _compute_S1(self):
        return 1 - self.kappa_t + 0.9 * (1 - self.rho_s / self.rho_f)

    def _compute_S2(self):
        out = 2 * self._f2.value - 1
        out *= 2 * self._f1.value

        out -= 4 * self._f4.value
        return out

    def _compute_S3(self):
        out = 3 - 1 / self._eta_t.value
        out *= -120 * (self._f3.value - self._f4.value)

        out += 50 * self._f1.value + 43 - 10 * self.kappa_t

        out *= self.rho_s - self.rho_f
        out /= 30 * self.rho_f * (3 + 2 / self._eta_t.value)

        return out

    def _compute_f1(self):
        return self._g1.value / self._g7.value

    def _compute_f2(self):
        if self._g1.value == 0:
            return 0
        return self._g2.value * self._g5.value / self._g1.value / 2

    def _compute_f3(self):
        return self._g3.value * self._g6.value / self._g7.value / 10

    def _compute_f4(self):
        return self._g4.value * self._g6.value / self._g7.value / 2

    def _compute_g1(self):
        return self._g5.value * self._g6.value

    def _compute_g2(self):
        out = 209 + 148 * self._eta_t.value + 48 / self._eta_t.value
        out *= -1 / 9 / self._zeta_t.value

        out += 19 + 38 * self._eta_t.value - 12 / self._eta_t.value
        return out

    def _compute_g3(self):
        out = 25 + 370 * self._eta_t.value - 80 / self._eta_t.value
        out *= 1 / 9 / self._zeta_t.value

        out -= (12 + 19 * self._eta_t.value + 4 / self._eta_t.value)
        return out

    def _compute_g4(self):
        out = 5 + 74 * self._eta_t.value - 16 / self._eta_t.value
        out *= 1 / 9 / self._zeta_t.value

        out -= (3 + 4 / self._eta_t.value)
        return out

    def _compute_g5(self):
        out = (1 - self._eta_t.value)
        out *= 19 + 16 / self._eta_t.value
        return out

    def _compute_g6(self):
        return 89 + 48 / self._eta_t.value + 38 * self._eta_t.value

    def _compute_g7(self):
        return self._g6.value**2

    @property
    def norm_delta(self) -> float:
        """ normalized viscous boundary thickness
        :math:`\\tilde{\\delta}=\\frac{\\delta}{R_0}`
        """
        return self._norm_delta.value

    def _compute_norm_delta(self):
        return self.delta / self.R_0

    @property
    def mu(self) -> float:
        """ (density * viscosity) ratio
        """
        return self._mu.value

    def _compute_mu(self):
        out = self.rho_f * self.eta_f
        out /= self.rho_s * self.eta_p
        return sqrt(out)

    @property
    def kappa_t(self) -> float:
        """ compressibility ratio
        """
        return self._kappa_t.value

    def _compute_kappa_t(self):
        return self.kappa_s / self.kappa_f

    @property
    def x_0(self) -> float:
        """ Real part of :attr:`~.x`
        """
        return self.x.real


if __name__ == '__main__':
    pass
