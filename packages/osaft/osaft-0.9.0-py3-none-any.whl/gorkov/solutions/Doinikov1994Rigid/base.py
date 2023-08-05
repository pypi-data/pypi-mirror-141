from __future__ import annotations

from typing import Optional, Union

from gorkov import log
from gorkov.core.backgroundfields import BackgroundField, WaveTypes
from gorkov.core.basecomposite import BaseSphereFrequencyComposite
from gorkov.core.fluids import ViscousFluid
from gorkov.core.frequency import Frequency
from gorkov.core.geometries import Sphere
from gorkov.core.solids import RigidSolid
from gorkov.core.variable import ActiveVariable, PassiveVariable
from gorkov.solutions.base_solution import BaseSolution


class BaseDoinikov1994Rigid(BaseSphereFrequencyComposite, BaseSolution):
    """Base class for Doinikov (viscous fluid-rigid sphere; 1994)

    :param frequency: Frequency [Hz]
    :param radius: Radius of the sphere [m]
    :param rho_s: Density of the fluid-like sphere [kg/m^3]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity [Pa s]
    :param zeta_f: bulk viscosity [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param wave_type: Type of wave, travel(l)ing or standing
    :param position: Position in the standing wave field [rad]
    :param N_max: Highest order mode
    """

    def __init__(
        self, frequency: Union[Frequency, float, int],
        radius: Union[Sphere, float, int],
        rho_s: float,
        rho_f: float, c_f: float,
        eta_f: float, zeta_f: float,
        p_0: float,
        wave_type: Optional[WaveTypes] = WaveTypes.STANDING,
        position: Optional[float] = None,
        N_max: int = 5,
    ) -> None:
        """Constructor method
        """

        # define name
        self._name = 'Doinikov1994Rigid'

        # init of parent class
        BaseSphereFrequencyComposite.__init__(self, frequency, radius)

        # Initialize Components
        self.scatterer = RigidSolid(self.frequency, rho_s)
        self.fluid = ViscousFluid(self.frequency, rho_f, c_f, eta_f, zeta_f)
        self.field = BackgroundField(self.fluid, p_0, wave_type, position)

        # Independent variables
        self._N_max = PassiveVariable(N_max, 'number of modes N')

        # Dependent Variables
        self._rho_t = ActiveVariable(
            self._compute_rho_t,
            'ratio of densities',
        )
        self._rho_t.is_computed_by(self.fluid._rho_f, self.scatterer._rho_s)

        if type(self) == BaseDoinikov1994Rigid:
            log.info(repr(self))

    def __repr__(self):
        return (
            f'BaseDoinikov1994Rigid(frequency={self.f}, radius={self.R_0}, '
            f'rho_s={self.rho_s}, rho_f={self.rho_f}, c_f={self.c_f}, '
            f'eta_f={self.eta_f}, zeta_f={self.zeta_f}, '
            f'p_0={self.p_0}, position={self.position}, {self.wave_type}, '
            f'N_max={self.N_max})'
        )

    @property
    def N_max(self):
        """Cutoff mode number for infinite sums

        :getter: returns number of infinite sum term
        :setter: automatically invokes
            :meth:`gorkov.core.variable.BaseVariable.notify`
        """
        return self._N_max.value

    @N_max.setter
    def N_max(self, value):
        self._N_max.value = value

    # -------------------------------------------------------------------------
    # Wrappers for Independent Field Attributes
    # -------------------------------------------------------------------------

    @property
    def position(self) -> float:
        """Wraps to
        :attr:`gorkov.core.backgroundfields.BackgroundField.position`
        """
        return self.field.position

    @position.setter
    def position(self, value: float) -> None:
        self.field.position = value

    @property
    def p_0(self) -> float:
        """Wraps to
        :attr:`gorkov.core.backgroundfields.BackgroundField.p_0`
        """
        return self.field.p_0

    @p_0.setter
    def p_0(self, value: float) -> None:
        self.field.p_0 = value

    @property
    def wave_type(self) -> WaveTypes:
        """ Wraps to
        :attr:`gorkov.core.backgroundfields.BackgroundField.wave_type`
        """
        return self.field.wave_type

    @wave_type.setter
    def wave_type(self, value: WaveTypes) -> None:
        self.field.wave_type = value

    # -------------------------------------------------------------------------
    # Wrappers for Independent Scatterer Attributes
    # -------------------------------------------------------------------------

    @property
    def rho_s(self) -> float:
        """ Wraps to :attr:`gorkov.core.solids.RigidSolid.rho_s`
        """
        return self.scatterer.rho_s

    @rho_s.setter
    def rho_s(self, value: float) -> None:
        self.scatterer.rho_s = value

    # -------------------------------------------------------------------------
    # Wrappers for Independent Fluid Attributes
    # -------------------------------------------------------------------------

    @property
    def rho_f(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.rho_f`
        """
        return self.fluid.rho_f

    @rho_f.setter
    def rho_f(self, value: float) -> None:
        self.fluid.rho_f = value

    @property
    def c_f(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.c_f`
        """
        return self.fluid.c_f

    @c_f.setter
    def c_f(self, value: float) -> None:
        self.fluid.c_f = value

    @property
    def eta_f(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.eta_f`
        """
        return self.fluid.eta_f

    @eta_f.setter
    def eta_f(self, value: float) -> None:
        self.fluid.eta_f = value

    @property
    def zeta_f(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.zeta_f`
        """
        return self.fluid.zeta_f

    @zeta_f.setter
    def zeta_f(self, value: float) -> None:
        self.fluid.zeta_f = value
    # -------------------------------------------------------------------------
    # Wrappers for Dependent Attributes
    # -------------------------------------------------------------------------

    @property
    def rho_t(self) -> float:
        """ Returns the ratio of the densities
        :math:`\\tilde{\\rho}=\\frac{\\rho_f}{\\rho_s}`
        """
        return self._rho_t.value

    def _compute_rho_t(self) -> float:
        return self.rho_f / self.rho_s

    # -------------------------------------------------------------------------
    # Wrappers for Dependent Fluid Attributes
    # -------------------------------------------------------------------------

    @property
    def kappa_f(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.kappa_f`
        """
        return self.fluid.kappa_f

    @property
    def k_f(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.k_f`
        """
        return self.fluid.k_f

    @property
    def k_v(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.k_v`
        """
        return self.fluid.k_v

    @property
    def delta(self) -> float:
        """ Wraps to :attr:`gorkov.core.fluids.ViscousFluid.delta`
        """
        return self.fluid.delta

    # -------------------------------------------------------------------------
    # Wrappers for Dependent Field Attributes
    # -------------------------------------------------------------------------

    @property
    def abs_pos(self) -> float:
        """Wraps to
        :attr:`gorkov.core.backgroundfields.BackgroundField.abs_pos`
        """
        return self.field.abs_pos

    def A_in(self, n) -> complex:
        """Wraps to
        :attr:`gorkov.core.backgroundfields.BackgroundField.A_in`
        """
        return self.field.A_in(n)


if __name__ == '__main__':
    pass
