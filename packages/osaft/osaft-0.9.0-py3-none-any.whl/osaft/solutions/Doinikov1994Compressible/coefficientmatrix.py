import numpy as np

from osaft.core.functions import SpecialFunctions as Sp
from osaft.core.functions import full_range
from osaft.core.variable import ActiveVariable


class CoefficientMatrix:
    """Matrix containing for the computation of scattering coefficients
    """

    def __init__(self) -> None:
        self._m_11 = ActiveVariable(self._reset_list, 'm_11 entry of matrix')
        self._m_12 = ActiveVariable(self._reset_list, 'm_12 entry of matrix')
        self._m_13 = ActiveVariable(self._reset_list, 'm_13 entry of matrix')
        self._m_14 = ActiveVariable(self._reset_list, 'm_14 entry of matrix')

        self._m_21 = ActiveVariable(self._reset_list, 'm_21 entry of matrix')
        self._m_22 = ActiveVariable(self._reset_list, 'm_22 entry of matrix')
        self._m_23 = ActiveVariable(self._reset_list, 'm_23 entry of matrix')
        self._m_24 = ActiveVariable(self._reset_list, 'm_24 entry of matrix')

        self._m_31 = ActiveVariable(self._reset_list, 'm_31 entry of matrix')
        self._m_32 = ActiveVariable(self._reset_list, 'm_32 entry of matrix')
        self._m_33 = ActiveVariable(self._reset_list, 'm_33 entry of matrix')
        self._m_34 = ActiveVariable(self._reset_list, 'm_34 entry of matrix')

        self._m_41 = ActiveVariable(self._reset_list, 'm_41 entry of matrix')
        self._m_42 = ActiveVariable(self._reset_list, 'm_42 entry of matrix')
        self._m_43 = ActiveVariable(self._reset_list, 'm_43 entry of matrix')
        self._m_44 = ActiveVariable(self._reset_list, 'm_44 entry of matrix')

        self._n_1 = ActiveVariable(self._reset_list, 'n_1 entry of RHS')
        self._n_2 = ActiveVariable(self._reset_list, 'n_2 entry of RHS')
        self._n_3 = ActiveVariable(self._reset_list, 'n_3 entry of RHS')
        self._n_4 = ActiveVariable(self._reset_list, 'n_4 entry of RHS')

    def det_M(self, n: int) -> complex:
        """det(M) of order :attr:`n`

        :param n: order
        """
        return np.linalg.det(self.M(n))

    def det_M_1(self, n: int) -> complex:
        """det(M_1) of order :attr:`n`

        :param n: order
        """
        return np.linalg.det(self.M_col(n, 1))

    def det_M_2(self, n: int) -> complex:
        """det(M_2) of order :attr:`n`

        :param n: order
        """
        return np.linalg.det(self.M_col(n, 2))

    def det_M_3(self, n: int) -> complex:
        """det(M_3) of order :attr:`n`

        :param n: order
        """
        return np.linalg.det(self.M_col(n, 3))

    def det_M_4(self, n: int) -> complex:
        """det(M_4) of order :attr:`n`

        :param n: order
        """
        return np.linalg.det(self.M_col(n, 4))

    def M(self, n: int) -> np.ndarray:
        """Matrix M of order :attr:`n`

        :param n: order
        """

        out = np.ndarray((4, 4), dtype=np.complex_)

        for i in full_range(1, 4):
            for j in full_range(1, 4):
                out[i - 1, j - 1] = getattr(self, f'm_{i}{j}')(n)

        return out

    def M_col(self, n: int, col: int) -> np.ndarray:
        """Matrix :math:`M_{col}` of order :attr:`n`

        :param n: order
        :param col: column that is replaced by RHS vector N
        """
        out = np.ndarray((4, 4), dtype=np.complex_)

        for i in full_range(1, 4):
            for j in full_range(1, 4):
                if j != col:
                    out[i - 1, j - 1] = getattr(self, f'm_{i}{j}')(n)
                else:
                    out[i - 1, j - 1] = getattr(self, f'n_{i}')(n)
        return out

    # -----------------------------------------------------------------------
    # RHS entries
    # -----------------------------------------------------------------------

    def n_1(self, n: int) -> complex:
        """Coefficient n_1 of RHS vector N of :attr:`n` th order

        :param n: order
        """
        if n < len(self._n_1.value):
            return self._n_1.value[n]
        else:
            self._compute_n_1(n)
            return self._n_1.value[n]

    def _compute_n_1(self, N: int) -> None:

        N_old = len(self._n_1.value)
        for n in full_range(N_old, N):
            out = -self.x * Sp.d1_besselj(n, self.x)
            out *= self.A_in(n)
            self._n_1.value.append(out)

    def n_2(self, n: int) -> complex:
        """Coefficient n_2 of RHS vector N of :attr:`n` th order

        :param n: order
        """
        if n < len(self._n_2.value):
            return self._n_2.value[n]
        else:
            self._compute_n_2(n)
            return self._n_2.value[n]

    def _compute_n_2(self, N: int) -> None:

        N_old = len(self._n_2.value)
        for n in full_range(N_old, N):
            out = -Sp.besselj(n, self.x)
            out *= self.A_in(n)
            self._n_2.value.append(out)

    def n_3(self, n: int) -> complex:
        """Coefficient n_3 of RHS vector N of :attr:`n` th order

        :param n: order
        """
        if n < len(self._n_3.value):
            return self._n_3.value[n]
        else:
            self._compute_n_3(n)
            return self._n_3.value[n]

    def _compute_n_3(self, N: int) -> None:

        N_old = len(self._n_3.value)
        for n in full_range(N_old, N):
            out = 1j * self.rho_f * self.c_f**2 / self.omega
            out += self.zeta_f
            out -= 2 / 3 * self.eta_f
            out *= Sp.besselj(n, self.x)

            out -= 2 * self.eta_f * Sp.d2_besselj(n, self.x)

            out *= self.A_in(n) * self.x**2
            self._n_3.value.append(out)

    def n_4(self, n: int) -> None:
        """Coefficient n_4 of RHS vector N of :attr:`n` th order

        :param n: order
        """
        if n < len(self._n_4.value):
            return self._n_4.value[n]
        else:
            self._compute_n_4(n)
            return self._n_4.value[n]

    def _compute_n_4(self, N: int) -> None:

        N_old = len(self._n_4.value)
        for n in full_range(N_old, N):
            out = Sp.besselj(n, self.x)
            out -= self.x * Sp.d1_besselj(n, self.x)

            out *= 2 * self.eta_f * self.A_in(n)
            self._n_4.value.append(out)
    # -----------------------------------------------------------------------
    # Matrix entries m_1j
    # -----------------------------------------------------------------------

    def m_11(self, n: int) -> None:
        """Coefficient m_11 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_11.value):
            return self._m_11.value[n]
        else:
            self._compute_m_11(n)
            return self._m_11.value[n]

    def _compute_m_11(self, N: int) -> None:
        N_old = len(self._m_11.value)
        for n in full_range(N_old, N):
            out = self.x * Sp.d1_hankelh1(n, self.x)

            self._m_11.value.append(out)

    def m_12(self, n: int) -> None:
        """Coefficient m_12 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_12.value):
            return self._m_12.value[n]
        else:
            self._compute_m_12(n)
            return self._m_12.value[n]

    def _compute_m_12(self, N: int) -> None:
        N_old = len(self._m_12.value)
        for n in full_range(N_old, N):
            out = -n * (n + 1) * Sp.hankelh1(n, self.x_v)

            self._m_12.value.append(out)

    def m_13(self, n: int) -> None:
        """Coefficient m_13 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_13.value):
            return self._m_13.value[n]
        else:
            self._compute_m_13(n)
            return self._m_13.value[n]

    def _compute_m_13(self, N: int) -> None:
        N_old = len(self._m_13.value)
        for n in full_range(N_old, N):
            out = - self.x_hat * Sp.d1_besselj(n, self.x_hat)

            self._m_13.value.append(out)

    def m_14(self, n: int) -> None:
        """Coefficient m_14 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_14.value):
            return self._m_14.value[n]
        else:
            self._compute_m_14(n)
            return self._m_14.value[n]

    def _compute_m_14(self, N: int) -> None:
        N_old = len(self._m_14.value)
        for n in full_range(N_old, N):
            out = n * (n + 1) * Sp.besselj(n, self.x_hat_v)

            self._m_14.value.append(out)

    # -----------------------------------------------------------------------
    # Matrix entries m_2j
    # -----------------------------------------------------------------------

    def m_21(self, n: int) -> None:
        """Coefficient m_21 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_21.value):
            return self._m_21.value[n]
        else:
            self._compute_m_21(n)
            return self._m_21.value[n]

    def _compute_m_21(self, N: int) -> None:
        N_old = len(self._m_21.value)
        for n in full_range(N_old, N):
            out = Sp.hankelh1(n, self.x)

            self._m_21.value.append(out)

    def m_22(self, n: int) -> None:
        """Coefficient m_22 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_22.value):
            return self._m_22.value[n]
        else:
            self._compute_m_22(n)
            return self._m_22.value[n]

    def _compute_m_22(self, N: int) -> None:
        N_old = len(self._m_22.value)
        for n in full_range(N_old, N):
            out = -Sp.hankelh1(n, self.x_v)
            out -= self.x_v * Sp.d1_hankelh1(n, self.x_v)

            self._m_22.value.append(out)

    def m_23(self, n: int) -> None:
        """Coefficient m_23 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_23.value):
            return self._m_23.value[n]
        else:
            self._compute_m_23(n)
            return self._m_23.value[n]

    def _compute_m_23(self, N: int) -> None:
        N_old = len(self._m_23.value)
        for n in full_range(N_old, N):
            out = -Sp.besselj(n, self.x_hat)

            self._m_23.value.append(out)

    def m_24(self, n: int) -> None:
        """Coefficient m_24 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_24.value):
            return self._m_24.value[n]
        else:
            self._compute_m_24(n)
            return self._m_24.value[n]

    def _compute_m_24(self, N: int) -> None:
        N_old = len(self._m_24.value)
        for n in full_range(N_old, N):
            out = Sp.besselj(n, self.x_hat_v)
            out += self.x_hat_v * Sp.d1_besselj(n, self.x_hat_v)

            self._m_24.value.append(out)

    # -----------------------------------------------------------------------
    # Matrix entries m_3j
    # -----------------------------------------------------------------------

    def m_31(self, n: int) -> None:
        """Coefficient m_31 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_31.value):
            return self._m_31.value[n]
        else:
            self._compute_m_31(n)
            return self._m_31.value[n]

    def _compute_m_31(self, N: int) -> None:
        N_old = len(self._m_31.value)
        for n in full_range(N_old, N):
            out = 1j * self.rho_f * self.c_f**2 / self.omega

            out += self.zeta_f
            out -= 2 / 3 * self.eta_f
            out *= -Sp.hankelh1(n, self.x)

            out += 2 * self.eta_f * Sp.d2_hankelh1(n, self.x)

            out *= self.x**2

            self._m_31.value.append(out)

    def m_32(self, n: int) -> None:
        """Coefficient m_32 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_32.value):
            return self._m_32.value[n]
        else:
            self._compute_m_32(n)
            return self._m_32.value[n]

    def _compute_m_32(self, N: int) -> None:
        N_old = len(self._m_32.value)
        for n in full_range(N_old, N):
            out = Sp.hankelh1(n, self.x_v)
            out -= self.x_v * Sp.d1_hankelh1(n, self.x_v)

            out *= 2 * n * (n + 1) * self.eta_f

            self._m_32.value.append(out)

    def m_33(self, n: int) -> None:
        """Coefficient m_33 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_33.value):
            return self._m_33.value[n]
        else:
            self._compute_m_33(n)
            return self._m_33.value[n]

    def _compute_m_33(self, N: int) -> None:
        N_old = len(self._m_33.value)
        for n in full_range(N_old, N):
            out = 1j * self.rho_s * self.c_s**2 / self.omega
            out += self.zeta_p
            out -= 2 / 3 * self.eta_p
            out *= Sp.besselj(n, self.x_hat)

            out -= 2 * self.eta_p * Sp.d2_besselj(n, self.x_hat)

            out *= self.x_hat**2

            self._m_33.value.append(out)

    def m_34(self, n: int) -> None:
        """Coefficient m_34 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_34.value):
            return self._m_34.value[n]
        else:
            self._compute_m_34(n)
            return self._m_34.value[n]

    def _compute_m_34(self, N: int) -> None:
        N_old = len(self._m_34.value)
        for n in full_range(N_old, N):
            out = self.x_hat_v * Sp.d1_besselj(n, self.x_hat_v)
            out -= Sp.besselj(n, self.x_hat_v)

            out *= 2 * n * (n + 1) * self.eta_p

            self._m_34.value.append(out)

    # -----------------------------------------------------------------------
    # Matrix entries m_4j
    # -----------------------------------------------------------------------

    def m_41(self, n: int) -> None:
        """Coefficient m_41 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_41.value):
            return self._m_41.value[n]
        else:
            self._compute_m_41(n)
            return self._m_41.value[n]

    def _compute_m_41(self, N: int) -> None:
        N_old = len(self._m_41.value)
        for n in full_range(N_old, N):
            out = self.x * Sp.d1_hankelh1(n, self.x)
            out -= Sp.hankelh1(n, self.x)

            out *= 2 * self.eta_f

            self._m_41.value.append(out)

    def m_42(self, n: int) -> None:
        """Coefficient m_42 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_42.value):
            return self._m_42.value[n]
        else:
            self._compute_m_42(n)
            return self._m_42.value[n]

    def _compute_m_42(self, N: int) -> None:
        N_old = len(self._m_42.value)
        for n in full_range(N_old, N):
            out = self.x_v**2 * Sp.d2_hankelh1(n, self.x_v)
            out += (n**2 + n - 2) * Sp.hankelh1(n, self.x_v)

            out *= -self.eta_f

            self._m_42.value.append(out)

    def m_43(self, n: int) -> None:
        """Coefficient m_43 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_43.value):
            return self._m_43.value[n]
        else:
            self._compute_m_43(n)
            return self._m_43.value[n]

    def _compute_m_43(self, N: int) -> None:
        N_old = len(self._m_43.value)
        for n in full_range(N_old, N):
            out = Sp.besselj(n, self.x_hat)
            out -= self.x_hat * Sp.d1_besselj(n, self.x_hat)

            out *= 2 * self.eta_p

            self._m_43.value.append(out)

    def m_44(self, n: int) -> None:
        """Coefficient m_44 of M matrix of :attr:`n` th order

        :param n: order
        """
        if n < len(self._m_44.value):
            return self._m_44.value[n]
        else:
            self._compute_m_44(n)
            return self._m_44.value[n]

    def _compute_m_44(self, N: int) -> None:
        N_old = len(self._m_44.value)
        for n in full_range(N_old, N):
            out = self.x_hat_v**2 * Sp.d2_besselj(n, self.x_hat_v)
            out += (n**2 + n - 2) * Sp.besselj(n, self.x_hat_v)

            out *= self.eta_p

            self._m_44.value.append(out)
