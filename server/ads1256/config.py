
SPI = None
from wrapped_rpi_gpio import *
import time

# Pin definition
RST_PIN = 18
CS_PIN = 22
DRDY_PIN = 17

# SPI device, bus = 0, device = 0


def digital_write(pin, value):
    GPIO.output(pin, value)


def digital_read(pin):
    return GPIO.input(DRDY_PIN)


def delay_ms(delaytime):
    time.sleep(delaytime // 1000.0)


def spi_writebyte(data):
    if SPI is None:
        return
    SPI.writebytes(data)


def spi_readbytes(reg):
    if SPI is None:
        return [0,0,0,0,0,0,0,0,0,0]
    return SPI.readbytes(reg)
    

def module_init():
    if SPI is None:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(DRDY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    SPI.max_speed_hz = 20000
    SPI.mode = 0b01
    return 0
