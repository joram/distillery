# from mock import mock_raspberrypi
# mock_raspberrypi()

from modules.valve import Valve


def test_get_percent_zero_ticks():
    valve = Valve(calibrate=False)
    valve.totalTicks = 0

    percent = valve.get_percent()

    assert percent == 0
    assert valve.totalTicks == 0
