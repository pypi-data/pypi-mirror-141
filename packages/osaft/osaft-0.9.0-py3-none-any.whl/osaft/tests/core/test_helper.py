import unittest

import numpy as np

from osaft.core.functions import pi
from osaft.core.helper import InputHandler as IH
from osaft.core.helper import RadiusTester as RT
from osaft.core.helper import ThetaTester as TT


class TestThetaTester(unittest.TestCase):

    def test_ValueError_float(self):
        self.assertRaises(ValueError, TT.test_theta, 1.01 * pi)
        self.assertRaises(ValueError, TT.test_theta, -0.1)

    def test_ValueError_int(self):
        self.assertRaises(ValueError, TT.test_theta, 4)
        self.assertRaises(ValueError, TT.test_theta, -1)

    def test_ValueError_np_ndarray(self):
        lst = [pi * np.random.rand() for _ in np.arange(10)]
        lst = np.asarray(lst)

        lst[2] = 1.01 * pi
        self.assertRaises(ValueError, TT.test_theta, lst)

        lst[2] = -1.01 * pi
        self.assertRaises(ValueError, TT.test_theta, lst)


class TestRadiusTesterInside(unittest.TestCase):

    def setUp(self):
        self.R_0 = 4 / 3

    def test_ValueError_float(self):
        self.assertRaises(ValueError, RT.is_inside_sphere, 1.01 * pi, self.R_0)
        self.assertRaises(ValueError, RT.is_inside_sphere, -0.1, self.R_0)

    def test_ValueError_int(self):
        self.assertRaises(ValueError, RT.is_inside_sphere, 4, self.R_0)
        self.assertRaises(ValueError, RT.is_inside_sphere, -1, self.R_0)

    def test_ValueError_np_ndarray(self):
        lst = [self.R_0 * np.random.rand() for _ in np.arange(10)]
        lst = np.asarray(lst)

        lst[2] = 1.01 * pi
        self.assertRaises(ValueError, RT.is_inside_sphere, lst, self.R_0)

        lst[2] = -1.01 * pi
        self.assertRaises(ValueError, RT.is_inside_sphere, lst, self.R_0)


class TestRadiusTesterOutside(unittest.TestCase):

    def setUp(self):
        self.R_0 = 4 / 3

    def test_ValueError_float(self):
        self.assertRaises(
            ValueError, RT.is_outside_sphere,
            0.1, self.R_0,
        )
        self.assertRaises(ValueError, RT.is_outside_sphere, -0.1, self.R_0)

    def test_ValueError_int(self):
        self.assertRaises(ValueError, RT.is_outside_sphere, 1, self.R_0)
        self.assertRaises(ValueError, RT.is_outside_sphere, -1, self.R_0)

    def test_ValueError_np_ndarray(self):
        lst = [self.R_0 * (1 + np.random.rand()) for _ in np.arange(10)]
        lst = np.asarray(lst)

        lst[2] = 0.99 * self.R_0
        lst[3] = 1.0 * self.R_0
        self.assertRaises(ValueError, RT.is_outside_sphere, lst, self.R_0)

        lst[2] = -1.01 * pi
        self.assertRaises(ValueError, RT.is_outside_sphere, lst, self.R_0)


class TestInputHandle(unittest.TestCase):

    def setUp(self):
        self.R_0 = 4 / 3

    def test_type(self):
        for var in [1, 1.2, [1, 2], (1, 2)]:
            self.assertTrue(isinstance(IH.handle_r(var, 3, True), np.ndarray))
            self.assertTrue(isinstance(IH.handle_r(var, 1, False), np.ndarray))
            self.assertTrue(
                isinstance(
                    IH.handle_theta(var),
                    np.ndarray,
                ),
            )

    def test_ValueError_float(self):
        self.assertRaises(ValueError, IH.handle_r, 0.1, self.R_0, False)
        self.assertRaises(ValueError, IH.handle_r, -0.1, self.R_0, False)
        self.assertRaises(ValueError, IH.handle_r, 2.1, self.R_0, True)
        self.assertRaises(ValueError, IH.handle_r, -2.1, self.R_0, True)

    def test_ValueError_int(self):
        self.assertRaises(ValueError, IH.handle_r, 1, self.R_0, False)
        self.assertRaises(ValueError, IH.handle_r, -1, self.R_0, False)
        self.assertRaises(ValueError, IH.handle_r, 2, self.R_0, True)
        self.assertRaises(ValueError, IH.handle_r, -2, self.R_0, True)

    def test_ValueError_list(self):
        lst = [self.R_0 * (1 + np.random.rand()) for _ in np.arange(10)]

        lst[2] = 0.99 * self.R_0
        lst[3] = 1.0 * self.R_0
        self.assertRaises(ValueError, IH.handle_r, lst, self.R_0, False)

        lst[2] = -1.01 * self.R_0
        self.assertRaises(ValueError, IH.handle_r, lst, self.R_0, True)

    def test_ValueError_np_ndarray(self):
        lst = [self.R_0 * (1 + np.random.rand()) for _ in np.arange(10)]
        lst = np.asarray(lst)

        lst[2] = 0.99 * self.R_0
        lst[3] = 1.0 * self.R_0
        self.assertRaises(ValueError, IH.handle_r, lst, self.R_0, False)

        lst[2] = -1.01 * pi
        self.assertRaises(ValueError, IH.handle_r, lst, self.R_0, False)


if __name__ == '__main__':
    unittest.main()
