from abc import abstractmethod

from osaft import WaveTypes


class HelperARF:
    """Baseclass for testing the ARF computation
    """
    _threshold = 1e-12

    @abstractmethod
    def compute_arf(self):
        pass

    def test_arf(self) -> None:
        self.do_testing(
            self.compute_arf, self.cls.acoustic_radiation_force,
            threshold=self._threshold,
            zero=1e-30,
        )


class HelperStandingARF(HelperARF):

    def test_arf(self) -> None:
        self.wave_type = WaveTypes.STANDING
        self._wave_type.list_of_values = [self.wave_type]
        HelperARF.test_arf(self)


class HelperTravelingARF(HelperARF):

    def test_arf(self) -> None:

        self.wave_type = WaveTypes.TRAVELLING
        self._wave_type.list_of_values = [self.wave_type]
        HelperARF.test_arf(self)


class HelperCompareARF:
    arf_compare_threshold = 1e-12

    def test_comparison_arf(self):
        self.do_testing(
            self.cls.acoustic_radiation_force,
            self.compare_cls.acoustic_radiation_force,
            threshold=self.arf_compare_threshold,
            zero=1e-30,
        )
