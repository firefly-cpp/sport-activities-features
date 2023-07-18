import os
from unittest import TestCase

from sport_activities_features import (
    BanisterTRIMPv1,
    BanisterTRIMPv2,
    EdwardsTRIMP,
    LuciaTRIMP,
    TCXFile,
)


class BanisterTRIMPv1TestCase(TestCase):

    """Banister's simple TRIMP test."""

    def setUp(self):
        """Setting up the test."""
        self.__banister = BanisterTRIMPv1(33.44, 165.22)

    def test_init_banister_trimp_works_fine(self):
        """Testing class arguments."""
        assert self.__banister.duration == 33.44
        assert self.__banister.average_heart_rate == 165.22

    def test_calculate_trimp_works_fine(self):
        """Testing Banister TRIMP."""
        val = self.__banister.calculate_TRIMP()
        assert val == 5524.9568


class BanisterTRIMPv2TestCase(TestCase):

    """Banister's TRIMP test."""

    def setUp(self):
        """Setting up the test."""
        self.__banister = BanisterTRIMPv2(duration=3240,
                                          average_heart_rate=117,
                                          min_heart_rate=77,
                                          max_heart_rate=173)

    def test_init_banister_trimp_v2_works_fine(self):
        """Testing class arguments."""
        assert self.__banister.duration == 3240
        assert self.__banister.average_heart_rate == 117
        assert self.__banister.rest_heart_rate == 77
        assert self.__banister.max_heart_rate == 173

    def test_calculate_trimp_v2_works_fine(self):
        """Testing Banister's v2 TRIMP."""
        val = self.__banister.calculate_TRIMP()
        assert val == 50.074670891080515


class EdwardsTRIMPTestCase(TestCase):

    """Edwards TRIMP test."""

    def setUp(self):
        """Setting up the test."""
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        activity = tcx_file.read_one_file(filename)
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
        activity = tcx_file.read_one_file(filename)
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
