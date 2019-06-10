# Replace libraries by fake ones
import sys
import fake_rpi


def mock_raspberrypi():
    sys.modules['RPi'] = fake_rpi.RPi      # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
