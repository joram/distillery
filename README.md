# Distillery
This software is intended to be run on a raspberrypi, with two hats, attached to a continuous run distillation appartatus.
The goals are to provide:
- a graph of temperatures along the fractionating column
- wash input rate control
- output valve control based on a target temperature at a target location

## Example Screenshot
![screenshot](/docs/screenshot.JPG)

## Hardware
![hardware diagram](/docs/distillery.jpg)
### Electronics
- A raspberryPi
- [Motor Controller HAT](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-dc-motors)
- [Analog to Digital HAT](https://www.waveshare.com/wiki/High-Precision_AD/DA_Board)
- a continuous run distillery

## setup

### On the PI
edit `/etc/rc.local`
add the lines:
```
sudo touch /var/log/distillery.log
sudo chmod 777 /var/log/distillery.log
sudo python /home/pi/code/distillery/server.py > /var/log/distillery.log &
```
reboot the pi

### python env
- install pyenv `curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`
- install python
    ```
    pyenv install 3.7.3
    pyenv virtualenv 3.7.3 distillery
    pyenv activate distillery
    pip install -r requirements.txt
    ```
- create the file `scripts/.env` and inside it add:

### install motor hat library
```
git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git
cd Adafruit-Motor-HAT-Python-Library
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo python setup.py install
```

### install AD hat library
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

### enable the hardware to recognize the i2c device
modify /boot/config.txt by appending
```
dtparam=i2c1=on
dtmparam=i2c_arm=on
```
