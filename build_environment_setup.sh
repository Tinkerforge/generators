#/bin/sh

# This script will create a folder named "tf" in your home directory,
# clone all of the tinkerforge gits, install all packages to build,
# the Bindings, the distribution zips, the documentation, Brick firmwares,
# Bricklet plugins, Brick Viewer and Brick Daemon.
# You will also be able to open, view and edit the schematics and layouts
# for Bricks and Bricklets as well as the design files of the cases.

# It was tested in a Ubuntu 15.04 VirtualBox image from osboxes.org.

cd ~
sudo apt-get update

# Packages for general use
sudo apt-get -y install git

# Packages for "generators/generate_all.py"
sudo apt-get -y install build-essential mono-complete python python3 perl default-jre default-jdk nodejs npm php5 php-pear ruby zip
sudo npm install -g browserify
sudo ln -s /usr/bin/nodejs /usr/local/bin/node

# Packages for "generators/test_all.py"
sudo apt-get -y install libxml2-utils libgd-dev

# Packages for "$:~/doc/ make html"
sudo apt-get -y install python-sphinx python-sphinxcontrib.spelling

# Packages for building and running brickv
sudo apt-get -y install python-qt4 python-qt4-gl python-opengl python-serial pyqt4-dev-tools

# Packages for building and running brickd
sudo apt-get -y install pkg-config libusb-1.0-0-dev libudev-dev pm-utils

# Packages for building Brick firmwares and Bricklet plugins
sudo apt-get -y install cmake gcc-arm-none-eabi

# Packages for hardware development (schematic, layout, case design)
sudo apt-get -y install kicad freecad

# Clone all necessary gits
gits=( "ac-current-bricklet" "accelerometer-bricklet" "ambient-light-bricklet" "ambient-light-v2-bricklet" "analog-in-bricklet" "analog-in-v2-bricklet" "analog-out-bricklet" "analog-out-v2-bricklet" "barometer-bricklet" "blinkenlights" "breakout-brick" "breakout-bricklet" "brickboot" "brickd" "brickletlib" "bricklib" "brickv" "cases" "chibi-extension" "color-bricklet" "co2-bricklet" "current12-bricklet" "current25-bricklet" "daemonlib" "dc-adapter" "dc-brick" "debug-brick" "distance-ir-bricklet" "distance-us-bricklet" "doc" "dual-button-bricklet" "dual-button-bricklet" "dual-relay-bricklet" "dust-detector-bricklet" "ethernet-extension" "gas-detector-bricklet" "generators" "gps-bricklet" "hall-effect-bricklet" "hardware-hacking" "heart-rate-bricklet" "humidity-bricklet" "imu-brick" "imu-v2-brick" "industrial-analog-out-bricklet" "industrial-digital-in-4-bricklet" "industrial-digital-out-4-bricklet" "industrial-dual-0-20ma-bricklet" "industrial-dual-analog-in-bricklet" "industrial-quad-relay-bricklet" "internet-of-things" "io16-bricklet" "io4-bricklet" "joystick-bricklet" "kicad-libraries" "laser-range-finder-bricklet" "lcd-16x2-bricklet" "lcd-20x4-bricklet" "led-strip-bricklet" "line-bricklet" "linear-poti-bricklet" "load-cell-bricklet" "master-brick" "moisture-bricklet" "motion-detector-bricklet" "multi-touch-bricklet" "nfc-rfid-bricklet" "oled-128x64-bricklet" "oled-64x48-bricklet" "ozone-bricklet" "piezo-buzzer-bricklet" "piezo-speaker-bricklet" "ptc-bricklet" "remote-switch-bricklet" "rotary-encoder-bricklet" "rotary-poti-bricklet" "rs232-bricklet" "rs485-extension" "segment-display-4x7-bricklet" "server-room-monitoring" "servo-brick" "solid-state-relay-bricklet" "sound-intensity-bricklet" "step-down-powersupply" "stepper-brick" "temperature-bricklet" "temperature-ir-bricklet" "thermocouple-bricklet" "tilt-bricklet" "tvpl-blockly" "tvpl-closure-library" "uv-light-bricklet" "voltage-bricklet" "voltage-current-bricklet" "weather-station" "wifi-extension" )

mkdir tf
cd tf

for g in "${gits[@]}"
do
	git clone https://github.com/Tinkerforge/$g.git
done

# Generate Bindings and Copy examples to documentation
cd ~/tf/generators/
python generate_all.py
python copy_all.py

# Generate doc
cd ~/tf/doc/
make html

# Generate brickv GUI
cd ~/tf/brickv/src/
python build_all_ui.py

# Build brickd
cd ~/tf/brickd/src/
ln -s ../../daemonlib/ .
cd ~/tf/brickd/src/brickd
make

# To show how it works we set up one Brick for use with kicad and one
# Brick as well as one Bricklet to compile with gcc.


# Build Master Brick
cd ~/tf/master-brick/software/src/
ln -s ../../../bricklib/ .
cd ~/tf/master-brick/software/
./generate_makefile
cd ~/tf/master-brick/software/build
make

# Build Temperature Bricklet
cd ~/tf/temperature-bricklet/software/src/
ln -s ../../../bricklib/ .
ln -s ../../../brickletlib/ .
cd ~/tf/temperature-bricklet/software/
./generate_makefile
cd ~/tf/temperature-bricklet/software/build
make

# Set up hardware design files for Master Brick
cd ~/tf/master-brick/hardware/
ln -s ../../kicad-libraries/ .
# To open schematics and layout:
# kicad ~/tf/master-brick/hardware/master.pro

# Cases can be found in ~/tf/cases and directly opend with freecad. e.g.:
# freecad ~/tf/cases/ambient_light/ambient_light.fcstd

cd ~
