from modules.base_module import BaseModule
import pins
try:
    from RPi import GPIO
except:
    print("faking rpi")
    import fake_rpi
    import sys
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)


class Relay(BaseModule):

    def __init__(self, name, pin=21):
        self.name = name
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self._is_on = False
        self.socket = None
        self.off()

    def on(self):
        GPIO.output(self.pin, GPIO.LOW)
        self._is_on = True
        if self.socket is not None:
            self.emit(self.socket)

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self._is_on = False
        if self.socket is not None:
            self.emit(self.socket)

    def emit(self, socket):
        self.socket = socket
        self._emit_value_update(socket, self.name, "enabled", self._is_on)


coolant_pump = Relay(pins.COOLANT_PUMP)
wash_pump = Relay(pins.WASH_PUMP)
