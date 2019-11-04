import importlib.util
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    print("faking rpi")
    import FakeRPi.GPIO as GPIO
