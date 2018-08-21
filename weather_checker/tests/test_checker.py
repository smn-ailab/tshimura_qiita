# -*- coding: utf-8 -*-

from unittest import TestCase

from nose.tools import eq_, ok_, raises, set_trace

from weather_checker.checker import create_message, get_information


class WeatherCheckerTestCase(TestCase):
    """Test case for weather checker."""

    @classmethod
    def setUpClass(self) -> None:
        """Run setup function just once, before all tests."""
        pass

    @classmethod
    def tearDownClass(self) -> None:
        """Run teardown function just once, after all tests."""
        pass

    @classmethod
    def setUp(self) -> None:
        """Run setup function before every test."""
        pass

    @classmethod
    def tearDown(self) -> None:
        """Run tear down function after every test."""
        pass

    def test_get_information(self) -> None:
        """Test function for get_information."""
        test_data = ["Hokkaido", "Okinawa"]
        answers = ["道央", "沖縄県"]
        for dat, ans in zip(test_data, answers):
            ret = get_information(dat)
            eq_(ret["place"], ans)

    @raises(ValueError)
    def test_get_information_error(self) -> None:
        """Test function for get_information (error case)."""
        get_information("California")

    def test_create_message(self) -> None:
        """Test function for create_message."""
        test_data = {
            "place": "東京都",
            "description": "天気概況のテスト",
            "forecasts": [
                {"weather": "晴れ", "temp_min": {"celsius": "30"}, "temp_max": {"celsius": "40"}},
                {"weather": "曇り", "temp_min": {"celsius": "20"}, "temp_max": {"celsius": "30"}},
                {"weather": "雨", "temp_min": {"celsius": "10"}, "temp_max": {"celsius": "20"}}]}

        ret = create_message(test_data)
        ok_(ret.find("東京都") > -1)
        ok_(ret.find("天気概況のテスト") > -1)
        ok_(ret.find("20℃") > -1)
