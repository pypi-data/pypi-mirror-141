import unittest

from numpy import real

from gorkov import Doinikov1994Compressible
from gorkov.core.backgroundfields import WaveTypes, WrongWaveTypeError
from gorkov.core.functions import pi, sin, sqrt
from gorkov.tests.basetest import BaseTest
from gorkov.tests.basetest_arf import HelperStandingARF, HelperTravelingARF


class TestARFBase(BaseTest):

    def setUp(self) -> None:

        super().setUp()

        self.small_viscous_boundary_layer = False
        self.gas_bubble = False
        self.small_particle_limit = True
        self.N_max = 5

        self.cls = Doinikov1994Compressible.ARF(
            self.f,
            self.R_0,
            self.rho_s, self.c_s, self.eta_p, self.zeta_p,
            self.rho_f, self.c_f, self.eta_f, self.zeta_f,
            self.p_0, self.wave_type,
            self.position,
            self.small_viscous_boundary_layer,
            self.gas_bubble,
            self.small_particle_limit,
            self.N_max,
        )

        self.list_cls = [self.cls]

    def assign_parameters(self) -> None:
        super().assign_parameters()

        self.cls.small_viscous_boundary_layer = (
            self.small_viscous_boundary_layer
        )
        self.cls.gas_bubble = self.gas_bubble
        self.cls.small_particle_limit = self.small_particle_limit
        self.cls.N_max = self.N_max

    @property
    def kappa_t(self) -> float:
        return self.rho_f * self.c_f**2 / self.rho_s / self.c_s**2

    @property
    def mu(self) -> float:
        return sqrt(self.rho_f * self.eta_f / self.rho_s / self.eta_p)

    @property
    def rho_t(self) -> float:
        return self.rho_f / self.rho_s

    @property
    def x_0(self) -> complex:
        return real(self.cls.field.k_f) * self.R_0

    @property
    def norm_delta(self) -> complex:
        return self.cls.delta / self.R_0

    def compute_g1(self):
        return self.compute_g5() * self.compute_g6()

    def compute_g2(self):
        out = 209 + 148 * self.compute_eta_t() + 48 / self.compute_eta_t()
        out *= - 1 / 9 / self.compute_zeta_t()

        out += 19 + 38 * self.compute_eta_t() - 12 / self.compute_eta_t()

        return out

    def compute_g3(self):
        out = 25 + 370 * self.compute_eta_t() - 80 / self.compute_eta_t()
        out *= 1 / 9 / self.compute_zeta_t()

        out += -12 - 19 * self.compute_eta_t() - 4 / self.compute_eta_t()

        return out

    def compute_g4(self):
        out = 5 + 74 * self.compute_eta_t() - 16 / self.compute_eta_t()
        out *= 1 / 9 / self.compute_zeta_t()

        out += -3 - 4 / self.compute_eta_t()

        return out

    def compute_g5(self):
        out = (1 - self.compute_eta_t())
        out *= (19 + 16 / self.compute_eta_t())
        return out

    def compute_g6(self):
        return 89 + 48 / self.compute_eta_t() + 38 * self.compute_eta_t()

    def compute_g7(self):
        return self.compute_g6()**2

    def compute_G(self):
        return (self.compute_S1() + self.compute_S2() + self.compute_S3()) / 3

    def compute_S1(self):
        return 1 - self.kappa_t + 0.9 * (1 - 1 / self.rho_t)

    def compute_S2(self):
        out = 2 * self.compute_f2() - 1
        out *= 2 * self.compute_f1()

        out -= 4 * self.compute_f4()
        return out

    def compute_S3(self):
        out = 3 - 1 / self.compute_eta_t()
        out *= -120 * (self.compute_f3() - self.compute_f4())

        out += 50 * self.compute_f1() + 43 - 10 * self.kappa_t

        out *= self.rho_s - self.rho_f
        out /= 30 * self.rho_f * (3 + 2 / self.compute_eta_t())

        return out

    def compute_f1(self):
        return self.compute_g1() / self.compute_g7()

    def compute_f2(self):
        if self.compute_g1() == 0:
            return 0
        return self.compute_g2() * self.compute_g5() / 2 / self.compute_g1()

    def compute_f3(self):
        return self.compute_g3() * self.compute_g6() / self.compute_g7() / 10

    def compute_f4(self):
        return self.compute_g4() * self.compute_g6() / self.compute_g7() / 2

    def compute_zeta_t(self):
        return self.zeta_p / self.zeta_f

    def compute_eta_t(self):
        return self.eta_p / self.eta_f


class TestARFMethods(TestARFBase):

    # ------------------

    def test_NotImplemented_solution(self) -> None:
        self.cls.wave_type = 'random'

        self.assertRaises(
            WrongWaveTypeError,
            self.cls.acoustic_radiation_force,
        )
    # ------------------

    def test_small_particle_limit(self) -> None:
        self.assign_parameters()
        self.assertEqual(
            self.small_particle_limit,
            self.cls.small_particle_limit,
        )

    def test_small_particle_limit_error(self) -> None:
        self.small_particle_limit = False
        self.assertRaises(NotImplementedError, self.assign_parameters)

    def test_small_viscous_boundary_layer(self) -> None:
        self.assign_parameters()
        self.assertEqual(
            self.small_viscous_boundary_layer,
            self.cls.small_viscous_boundary_layer,
        )
        self.small_viscous_boundary_layer = True
        self.assign_parameters()
        self.assertEqual(
            self.small_viscous_boundary_layer,
            self.cls.small_viscous_boundary_layer,
        )

    def test_gas_bubble(self) -> None:
        self.gas_bubble = False
        self.assign_parameters()
        self.assertEqual(
            self.gas_bubble,
            self.cls.gas_bubble,
        )
        self.gas_bubble = True
        self.assertRaises(NotImplementedError, self.assign_parameters)

    def test_liquid_liquid_NotImplementedError(self):
        self.wave_type = WaveTypes.STANDING
        self.small_viscous_boundary_layer = False
        self.assign_parameters()

        self.assertRaises(
            NotImplementedError,
            self.cls.acoustic_radiation_force,
        )

    def test_g1(self):
        self.do_testing(
            func_2=self.compute_g1,
            func_1=lambda: self.cls._g1.value,
        )

    def test_g2(self):
        self.do_testing(
            func_2=self.compute_g2,
            func_1=lambda: self.cls._g2.value,
        )

    def test_g3(self):
        self.do_testing(
            func_2=self.compute_g3,
            func_1=lambda: self.cls._g3.value,
        )

    def test_g4(self):
        self.do_testing(
            func_2=self.compute_g4,
            func_1=lambda: self.cls._g4.value,
        )

    def test_g5(self):
        self.do_testing(
            func_2=self.compute_g5,
            func_1=lambda: self.cls._g5.value,
        )

    def test_g6(self):
        self.do_testing(
            func_2=self.compute_g6,
            func_1=lambda: self.cls._g6.value,
        )

    def test_g7(self):
        self.do_testing(
            func_2=self.compute_g7,
            func_1=lambda: self.cls._g7.value,
        )

    def test_G(self):
        self.do_testing(
            func_2=self.compute_G,
            func_1=lambda: self.cls._G.value,
        )

    def test_S1(self):
        self.do_testing(
            func_2=self.compute_S1,
            func_1=lambda: self.cls._S1.value,
        )

    def test_S2(self):
        self.do_testing(
            func_2=self.compute_S2,
            func_1=lambda: self.cls._S2.value,
        )

    def test_S3(self):
        self.do_testing(
            func_2=self.compute_S3,
            func_1=lambda: self.cls._S3.value,
        )

    def test_f1(self):
        self.do_testing(
            func_2=self.compute_f1,
            func_1=lambda: self.cls._f1.value,
        )

    def test_f2(self):
        self.do_testing(
            func_2=self.compute_f2,
            func_1=lambda: self.cls._f2.value,
        )
        # if statement --> eta_t must be = 1
        self.eta_f = self.eta_p
        self.assign_parameters()
        self.do_testing(
            func_2=self.compute_f2,
            func_1=lambda: self.cls._f2.value,
        )

    def test_f3(self):
        self.do_testing(
            func_2=self.compute_f3,
            func_1=lambda: self.cls._f3.value,
        )

    def test_f4(self):
        self.do_testing(
            func_1=self.compute_f4,
            func_2=lambda: self.cls._f4.value,
        )

    def test_zeta_t(self):
        self.do_testing(
            func_2=self.compute_zeta_t,
            func_1=lambda: self.cls._zeta_t.value,
        )

    def test_eta_t(self):
        self.do_testing(
            func_2=self.compute_eta_t,
            func_1=lambda: self.cls._eta_t.value,
        )

    def test_propertiess(self) -> None:
        properties = ['x_0', 'norm_delta', 'kappa_t', 'mu']
        self._test_properties(properties)


# |x| << 1 << |x_v|
# |x_s| << 1 << |x_v_s|
# kappa_t << 1
# mu << 1

class TestARFLimit1Traveling(HelperTravelingARF, TestARFBase):

    def setUp(self) -> None:
        TestARFBase.setUp(self)
        self.gas_bubble = False
        self.small_viscous_boundary_layer = False
        self.small_particle_limit = True

    def compute_arf(self):
        out = 6 * pi * self.rho_f * self.x_0**3 * self.cls.field.abs_A_squared
        out *= self.norm_delta * (self.rho_s - self.rho_f)**2
        out /= (1 + self.mu) * (2 * self.rho_s + self.rho_f)**2

        return out


# |x| << |x_v| << 1
# |x_s | << | x_v_s | << 1
# kappa_t << 1
# rho_f << rho_s

class TestARFLimit2Traveling(HelperTravelingARF, TestARFBase):

    def setUp(self) -> None:
        TestARFBase.setUp(self)
        self.gas_bubble = False
        self.small_viscous_boundary_layer = True
        self.small_particle_limit = True

    def compute_arf(self):
        out = pi / 6 * self.rho_f * self.x_0**3 * self.cls.field.abs_A_squared
        out *= self.norm_delta**2
        out *= 5 - 2 * self.kappa_t - 8 * self.compute_f1()

        return out


class TestARFLimit2Standing(HelperStandingARF, TestARFBase):

    def setUp(self) -> None:
        TestARFBase.setUp(self)
        self.gas_bubble = False
        self.small_viscous_boundary_layer = True
        self.small_particle_limit = True

    def compute_arf(self):
        out = pi * self.rho_f * self.x_0**3 * self.cls.field.abs_A_squared
        out *= self.compute_G() * sin(2 * self.position * self.cls.k_f.real)

        return out


if __name__ == '__main__':
    unittest.main()
