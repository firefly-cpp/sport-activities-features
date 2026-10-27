import math
import os
from unittest import TestCase

from sport_activities_features import (
    BanisterTRIMPv2,
    EdwardsTRIMP,
    Gender,
    LuciaTRIMP,
    TCXFile,
)


class BanisterTRIMPv2TestCase(TestCase):

    """Banister's TRIMP test."""

    def setUp(self):
        """Setting up the test."""
        self.__banister = BanisterTRIMPv2(duration=3240,
                                          average_heart_rate=117,
                                          rest_heart_rate=77,
                                          max_heart_rate=173)

    def test_init_banister_trimp_v2_works_fine(self):
        """Testing class arguments."""
        assert self.__banister.duration == 3240
        assert self.__banister.average_heart_rate == 117
        assert self.__banister.rest_heart_rate == 77
        assert self.__banister.max_heart_rate == 173
        assert self.__banister.gender is Gender.male

    def test_calculate_trimp_v2_works_fine(self):
        """Testing Banister's v2 TRIMP.

        54 min, dHR = (117 - 77) / (173 - 77) = 0.41667:
        54 * 0.41667 * 0.64 * e^(1.92 * 0.41667) = 32.0478
        """
        val = self.__banister.calculate_TRIMP()
        self.assertAlmostEqual(
            val, 54 * (40 / 96) * 0.64 * math.exp(1.92 * 40 / 96),
        )
        self.assertAlmostEqual(val, 32.0478, places=4)

    def test_female(self):
        val = BanisterTRIMPv2(
            3240, 117, 77, 173, gender=Gender.female,
        ).calculate_TRIMP()
        self.assertAlmostEqual(
            val, 54 * (40 / 96) * 0.86 * math.exp(1.67 * 40 / 96),
        )

    def test_one_hour_at_maximum_heart_rate(self):
        # dHR = 1: 60 * 0.64 * e^1.92 = 261.92 (men), 60 * 0.86 * e^1.67
        # = 274.11 (women)
        male = BanisterTRIMPv2(3600, 190, 50, 190).calculate_TRIMP()
        female = BanisterTRIMPv2(
            3600, 190, 50, 190, Gender.female,
        ).calculate_TRIMP()
        self.assertAlmostEqual(male, 261.92, places=2)
        self.assertAlmostEqual(female, 274.11, places=2)

    def test_positional_arguments(self):
        positional = BanisterTRIMPv2(3240, 117, 77, 173)
        self.assertEqual(positional.rest_heart_rate, 77)
        self.assertAlmostEqual(
            positional.calculate_TRIMP(), self.__banister.calculate_TRIMP(),
        )

    def test_min_heart_rate_is_deprecated(self):
        with self.assertWarns(DeprecationWarning):
            banister = BanisterTRIMPv2(
                duration=3240, average_heart_rate=117,
                min_heart_rate=77, max_heart_rate=173,
            )
        self.assertEqual(banister.rest_heart_rate, 77)
        self.assertAlmostEqual(
            banister.calculate_TRIMP(), self.__banister.calculate_TRIMP(),
        )

    def test_invalid_arguments(self):
        with self.assertRaises(TypeError):
            BanisterTRIMPv2(3240, 117)
        with self.assertRaises(TypeError):
            BanisterTRIMPv2(
                3240, 117, rest_heart_rate=77, max_heart_rate=173,
                min_heart_rate=77,
            )
        with self.assertRaises(ValueError):
            BanisterTRIMPv2(3240, 117, 173, 173)


class EdwardsTRIMPTestCase(TestCase):

    """Edwards TRIMP test."""

    def setUp(self):
        """Setting up the test."""
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        tcx_exercise = tcx_file.read_one_file(filename)
        activity = tcx_file.extract_activity_data(tcx_exercise)
        timestamps = activity['timestamps']
        heart_rates = activity['heartrates']
        self.__edwards = EdwardsTRIMP(heart_rates, timestamps, 200)

    def test_init_banister_trimp_works_fine(self):
        """Testing class arguments."""
        assert len(self.__edwards.heart_rates) == 7799
        assert len(self.__edwards.timestamps) == 7799
        assert self.__edwards.max_heart_rate == 200

    def test_calculate_trimp_works_fine(self):
        """Testing Edwards TRIMP."""
        val = self.__edwards.calculate_TRIMP()
        assert val == 41458


class LuciaTRIMPTestCase(TestCase):

    """Lucia's TRIMP test."""

    def setUp(self):
        """Setting up the test."""
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        tcx_exercise = tcx_file.read_one_file(filename)
        activity = tcx_file.extract_activity_data(tcx_exercise)
        timestamps = activity['timestamps']
        heart_rates = activity['heartrates']
        self.__lucia = LuciaTRIMP(heart_rates, timestamps, VT1=160, VT2=180)

    def test_init_banister_trimp_works_fine(self):
        """Testing class arguments."""
        assert len(self.__lucia.heart_rates) == 7799
        assert len(self.__lucia.timestamps) == 7799
        assert 160 == self.__lucia.VT1
        assert 180 == self.__lucia.VT2

    def test_calculate_trimp_works_fine(self):
        """Testing Lucia's TRIMP."""
        val = self.__lucia.calculate_TRIMP()
        assert val == 19251
