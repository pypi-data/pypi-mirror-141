import unittest

import numpy as np

from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.tests.basetest import NumericTestCase


class TestVariables(NumericTestCase):

    def test_hierarchy(self) -> None:
        P1 = PassiveVariable(-3.0)
        P2 = PassiveVariable(+3.0)

        def compute_A():
            return P1.value + P2.value

        A = ActiveVariable(compute_A)
        A.is_computed_by(P1, P2)

        def compute_B():
            return A.value - P2.value - P1.value

        B = ActiveVariable(compute_B)

        B.is_computed_by(A, P1, P2)

        # initial check
        self.assertEqual(0.0, A.value)
        self.assertEqual(0.0, B.value)
        # change a value and check
        P1.value = 0
        self.assertEqual(0.0, B.value)

    def test_exception_when_linking(self):

        P1 = PassiveVariable(-3.0)
        P2 = PassiveVariable(+3.0)

        def compute_A():
            return P1.value + P2.value

        A = ActiveVariable(compute_A)

        A.is_computed_by(P1, P2)

        self.assertRaises(TypeError, A.is_computed_by, P1, 1)

    def test_no_argument_exception(self):

        P1 = PassiveVariable(-3.0)
        P2 = PassiveVariable(+3.0)

        def compute_A():
            return P1.value + P2.value

        A = ActiveVariable(compute_A)

        self.assertRaises(TypeError, A.is_computed_by)

    def test_variable_name(self):

        P1_name = 'P1'
        P1 = PassiveVariable(1, P1_name)
        self.assertEqual(P1.name, P1_name)

        P2 = PassiveVariable(1)
        self.assertEqual(P2.name, 'Unnamed')

        self.assertRaises(TypeError, PassiveVariable, 1, 1)

    def test_non_single_argument(self) -> None:
        # initial assignment
        P1 = PassiveVariable([1, 2], 'list')
        self.assertEqual(P1.value, [1, 2])
        # change list
        P1.value = [2, 3]
        self.assertEqual(P1.value, [2, 3])
        # longer list
        P1.value = [1, 2, 3]
        self.assertEqual(P1.value, [1, 2, 3])
        # same list
        P1.value = [1, 2, 3]
        self.assertEqual(P1.value, [1, 2, 3])
        # np.array
        val = np.asarray([1, 2, 3])
        P1.value = val
        self.assertTrue(np.alltrue(P1.value == val))
        # change from list to single value
        val = -10.0
        P1.value = val
        self.assertEqual(P1.value, val)
        # change from single value to list
        val = np.asarray([-1, 2.7, 3])
        P1.value = val
        self.assertTrue(np.alltrue(P1.value == val))
        # different order in list
        val = np.asarray([-1, 2.7, 3])
        P1.value = np.asarray([2.7, 3, -1])
        self.assertFalse(np.alltrue(P1.value == val))


class TestActiveVariable(unittest.TestCase):

    def test_needs_update(self):
        self.P1 = PassiveVariable(-1)
        self.P2 = PassiveVariable(1.0)
        self.P3 = PassiveVariable(np.pi)

        self.A = ActiveVariable(lambda: True)
        self.A.is_computed_by(self.P1, self.P2, self.P3)
        self.assertTrue(self.A.needs_update)
        _ = self.A.value
        self.assertFalse(self.A.needs_update)
        for P in [self.P1, self.P2, self.P3]:
            P.value = 42
            self.assertTrue(self.A.needs_update)
            _ = self.A.value
            self.assertFalse(self.A.needs_update)


if __name__ == '__main__':
    unittest.main()
