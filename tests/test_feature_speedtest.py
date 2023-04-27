import pytest

from src.features.speedtest import SpeedTester


class TestSpeedTester:
    def test_speed_test(self):
        """Tests the speed_check function."""

        speedtest = SpeedTester()
        speedtest_result = speedtest.speed_check()

        assert isinstance(speedtest_result, str)
