from collections.abc import Sequence
from enum import Enum
from numbers import Number
from typing import Optional, Union

import numpy as np

from gorkov.core.functions import pi


class StringFormatter:
    """ Consistent Formatting for __str__ and __repr__ methods
    """

    @staticmethod
    def get_str_text(
        description: str, variable: str,
        value: Union[float, int, str], unit: Optional[str] = None,
        linebreak: bool = True,
    ) -> str:
        """
        Returns a constant formatting for the `__str__` method of the ARF
        classes

        :param description: Physical name for the variable
        :param variable: symbol/name of the variable
        :param value: value of the variable
        :param unit: unit of the variable
        :param linebreak: Appends a linebreak to the end of the text
        """
        out = f'{description:<20s}:\t'
        out += f'{variable:>8s} = '
        if isinstance(value, bool) or value is None:
            out += str(value)
        elif isinstance(value, Enum):
            out += f'{value.name:8s}'
        else:
            out += f'{value:5.2e}'
        if unit is not None and unit != '':
            out += f' [{unit:s}]'
        if linebreak:
            out += '\n'

        return out


class BaseValueTester:
    """ BaseClass for input value testing
    """

    low = None
    high = None
    msg = None

    @classmethod
    def test_arg(cls, arg: np.ndarray) -> None:
        """ Tests if (any value of) :attr:`arg` is between
        :attr:`cls.low` and :attr:`cls.high`

        :param arg: array to be tested
        :raises: ValueError if test fails
        """
        if np.any(arg > cls.high) > 0 or np.any(arg < cls.low):
            raise ValueError(cls.msg)


class ThetaTester(BaseValueTester):
    """ Test if  :math:`0 <= \\theta <= \\pi`
    """

    @classmethod
    def test_theta(cls, theta: Union[Number, np.ndarray]) -> None:
        """ Tests :attr:`theta` value is between 0 and :math:`\\pi`

        :param theta: input angles
        :raises: ValueError if  at least one theta is > pi or < 0
        """
        cls.low = 0
        cls.high = pi
        cls.msg = 'At least on theta values is greater '
        cls.msg += 'than pi or smaller than zero.'
        ThetaTester.test_arg(theta)


class RadiusTester(BaseValueTester):
    """ Test if  :math:`r` is inside or outside of sphere
    """

    @classmethod
    def is_inside_sphere(cls, r: Union[Number, np.array], R_0: float) -> None:
        """ Tests :attr:`r` value is between 0 and :attr:`R_0`

        :param r: input radii
        :param R_0: particle radius
        :raises: ValueError if  at least one theta is > R_0 or < 0
        """
        cls.low = 0
        cls.high = R_0
        cls.msg = 'At least one value of r is negative and/or greater '
        cls.msg += 'greater than R_0'
        RadiusTester.test_arg(r)

    @classmethod
    def is_outside_sphere(
        cls, r: Union[Number, np.ndarray],
        R_0: float,
    ) -> None:

        """ Tests :attr:`r` value is greater than :attr:`R_0`

        :param r: input radii
        :param R_0: particle radius
        :raises: ValueError if  at least one r < R_0
        """
        cls.low = R_0
        cls.high = np.Infinity
        cls.msg = 'At least one value of r is smaller than R_0'
        RadiusTester.test_arg(r)


class InputHandler:
    """ Handles inputs for velocity field methods

    Tests if inputs r, theta, t passed to methods that compute the velocity
    field are valid inputs and converts the inputs to numpy.ndarray.
    """

    test_theta = ThetaTester.test_theta
    test_r_inside = RadiusTester.is_inside_sphere
    test_r_outside = RadiusTester.is_outside_sphere

    @classmethod
    def handle_input(
        cls, r: Union[Number, Sequence],
        theta: Union[Number, Sequence],
        t: Union[Number, Sequence],
        R_0: Union[Number, Sequence],
        inside_sphere: bool,
    ):
        """Tests if inputs r, theta, t passed to methods that compute the
        velocity field are valid inputs and converts the
        inputs to numpy.ndarray.

        :param r: radial coordinate
        :param theta: tangential coordinate
        :param t: time
        :param R_0: radius of the sphere
        :param inside_sphere: if `True`/`False` tests if `r` is inside/outside
        """
        r = cls.handle_r(r, R_0, inside_sphere)
        theta = cls.handle_theta(theta)
        t = cls._to_array(t)

        return r, theta, t

    @classmethod
    def handle_r(cls, r, R_0, inside_sphere):
        """Tests if inputs `r` is inside or outside sphere and converts input
        to numpy.ndarray

        :param r: radial coordinate
        :param R_0: radius of the sphere
        :param inside_sphere: if `True`/`False` tests if `r` is inside/outside
        """
        r = cls._to_array(r)
        if inside_sphere:
            cls.test_r_inside(r, R_0)
        else:
            cls.test_r_outside(r, R_0)
        return r

    @classmethod
    def handle_theta(cls, theta):
        """Tests if inputs `theta` is between 0 and :math:`\\pi` input to
        numpy.ndarray

        :param theta: tangential coordinate
        """

        theta = cls._to_array(theta)
        cls.test_theta(theta)
        return theta

    @staticmethod
    def _to_array(arg: [Number, Sequence]):
        return np.asarray(arg)


if __name__ == '__main__':
    pass
