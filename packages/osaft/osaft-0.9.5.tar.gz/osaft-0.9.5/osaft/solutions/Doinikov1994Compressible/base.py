from typing import Optional, Union

from osaft.core.backgroundfields import WaveTypes
from osaft.core.fluids import ViscousFluid
from osaft.core.frequency import Frequency
from osaft.core.geometries import Sphere
from osaft.core.helper import StringFormatter as SF
from osaft.solutions.Doinikov1994Rigid.base import BaseDoinikov1994Rigid


class BaseDoinikov1994Compressible(BaseDoinikov1994Rigid):
    """Base class for Doinikov (viscous fluid-viscous sphere; 1994)

    :param frequency: Frequency [Hz]
    :param radius: Radius of the solid [m]
    :param rho_s: Density of the fluid-like solid [kg/m^3]
    :param c_s: Speed of sound of the sphere [m/s]
    :param eta_s: shear viscosity of the sphere [Pa s]
    :param zeta_s: bulk viscosity of the sphere [Pa s]
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
        rho_s: float, c_s: float, eta_s: float, zeta_s: float,
        rho_f: float, c_f: float, eta_f: float, zeta_f: float,
        p_0: float, wave_type: WaveTypes, position: float,
        N_max: Optional[int] = 3,
    ) -> None:
        """Constructor method
        """

        super().__init__(
            frequency, radius, rho_s, rho_f, c_f, eta_f, zeta_f,
            p_0, position, wave_type, N_max,
        )

        self.scatterer = ViscousFluid(
            self.frequency, rho_s, c_s, eta_s,
            zeta_s,
        )

    def __str__(self):
        out = 'Doinikovs\'s  (1994) model (viscous fluid-viscous sphere)'
        out += ' with the following properties: \n'
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
            'Shear viscosity', 'eta_s',
            self.eta_s, '1/Pa',
        )
        out += SF.get_str_text(
            'Bulk viscosity', 'zeta_s',
            self.zeta_s, '1/Pa',
        )
        return out

    # -------------------------------------------------------------------------
    # Wrappers for Independent sphere Attributes
    # -------------------------------------------------------------------------

    @property
    def kappa_s(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.kappa_f`
        """
        return self.scatterer.kappa_f

    @property
    def k_s(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.k_f`
        """
        return self.scatterer.k_f

    @property
    def k_vs(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.k_v`
        """
        return self.scatterer.k_v

    @property
    def rho_s(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.rho_f`
        """
        return self.scatterer.rho_f

    @rho_s.setter
    def rho_s(self, value: float) -> None:
        self.scatterer.rho_f = value

    @property
    def c_s(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.c_f`
        """
        return self.scatterer.c_f

    @c_s.setter
    def c_s(self, value: float) -> None:
        self.scatterer.c_f = value

    @property
    def eta_s(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.eta_f`
        """
        return self.scatterer.eta_f

    @eta_s.setter
    def eta_s(self, value: float) -> None:
        self.scatterer.eta_f = value

    @property
    def zeta_s(self) -> float:
        """ Wraps to :attr:`osaft.core.fluids.ViscousFluid.zeta_f`
        """
        return self.scatterer.zeta_f

    @zeta_s.setter
    def zeta_s(self, value: float) -> None:
        self.scatterer.zeta_f = value


if __name__ == '__main__':
    pass
