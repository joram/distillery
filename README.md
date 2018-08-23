# hardware
[Motor Controller HAT](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-dc-motors)
[Analog to Digital HAT](https://www.waveshare.com/wiki/High-Precision_AD/DA_Board)


# setup

## install motor hat library
```
git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git
cd Adafruit-Motor-HAT-Python-Library
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo python setup.py install
```

## install AD hat library
```
# setup C library
sudo apt-get install automake libtool
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.50.tar.gz
tar zxvf bcm2835-1.50.tar.gz
cd bcm2835-1.50
autoreconf -vfi
./configure
make
sudo make check
sudo make install

# setup python library
sudo apt-get install git build-essential python-dev
cd ~
git clone https://github.com/fabiovix/py-ads1256.git
cd py-ads1256
sudo python setup.py install
```
