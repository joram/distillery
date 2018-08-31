import time
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Button(object):

  def __init__(self, pin, sleep_ms=500):
    self.pin = pin
    self.value = -1
    self.sleep_ms = sleep_ms
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    self._thread = threading.Thread(target=self._poll_thread, args=())
    self._thread.daemon = True
    self._thread.start()

  def _poll_thread(self):
    while True:
      self.value = GPIO.input(self.pin)
      time.sleep(self.sleep_ms/1000)

  @property
  def pressed(self):
    return self.value == 0
