sudo apt-get install vim python-pip
sudo apt-get install automake libtool
sudo apt-get install git build-essential python-dev

# C drivers
cd ~
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.56.tar.gz
tar zxvf bcm2835-1.56.tar.gz
cd bcm2835-1.56
./configure
make
sudo make check
sudo make install


# python lib
cd ~
git clone https://github.com/fabiovix/py-ads1256.git
cd py-ads1256
sudo python setup.py install
