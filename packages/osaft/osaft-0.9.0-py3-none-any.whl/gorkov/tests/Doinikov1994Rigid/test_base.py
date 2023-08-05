import unittest

from gorkov.solutions.Doinikov1994Rigid.base import BaseDoinikov1994Rigid
from gorkov.tests.basetest import BaseTest


class TestBase(BaseTest):
    def setUp(self) -> None:
        super().setUp()

        self.cls = BaseDoinikov1994Rigid(
            self.f, self.R_0, self.rho_s,
            self.rho_f, self.c_f,
            self.eta_f, self.zeta_f,
            self.p_0, self.wave_type,
            self.position,
        )

    @property
    def rho_t(self) -> float:
        return self.rho_f / self.rho_s

    def test_properties(self) -> None:
        properties = ['rho_t']
        self._test_properties(properties)


if __name__ == '__main__':
    unittest.main()
