from unittest import TestCase
from sport_activities_features.training_loads import BanisterTRIMP


class BanisterTRIMPTestCase(TestCase):
    def setUp(self):
        self.__banister = BanisterTRIMP(33.44, 165.22)

    def test_init_banister_trimp_works_fine(self):
        self.assertEqual(33.44, self.__banister.duration)
        self.assertEqual(165.22, self.__banister.avg_hr)

    def test_calculate_trimp_works_fine(self):
        val = self.__banister.calculate_TRIMP()
        self.assertEqual(5524.9568, val)
