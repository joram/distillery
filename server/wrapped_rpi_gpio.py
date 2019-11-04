try:
    from RPi import GPIO
    GPIO.setwarnings(False)
    valve_calibrate = True
except:
    print("faking rpi")
    import fake_rpi
    import sys
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
    fake_rpi.toggle_print(False)
    valve_calibrate = False
