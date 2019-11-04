from modules.button import Button, _pin_changed
from wrapped_rpi_gpio import GPIO
import mock

def test_default_button_unpressed():
    button = Button(1)

    assert not button.is_pressed


def test_default_button_pressed():
    GPIO.input = mock.Mock(return_value=1)
    button = Button(1)

    assert button.is_pressed


def test_button_unpressed():
    GPIO.input = mock.Mock(return_value=1)
    button = Button(1)
    GPIO.input = mock.Mock(return_value=0)
    _pin_changed(1)

    assert not button.is_pressed


