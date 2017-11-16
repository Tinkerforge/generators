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
sudo apt-get -y install python git

# Packages for "generators/generate_all.py"
sudo apt-get -y install php5 # in older Ubuntu there was a package named php5
sudo apt-get -y install php # in newer Ubuntu there is a meta package named php that depends on php7.0
sudo apt-get -y install build-essential mono-complete mono-reference-assemblies-2.0 python3 perl default-jre default-jdk nodejs npm php-pear ruby zip
sudo npm install -g browserify
sudo ln -s /usr/bin/nodejs /usr/local/bin/node

# Packages for "generators/test_all.py"
sudo apt-get -y install libxml2-utils libgd-dev

# Packages for "$:~/doc/ make html"
sudo apt-get -y install python-sphinx python-sphinxcontrib.spelling

# Packages for building and running brickv
sudo apt-get -y install python-qt4 python-qt4-gl python-opengl python-serial python-setuptools pyqt4-dev-tools

# Packages for building and running brickd
sudo apt-get -y install pkg-config libusb-1.0-0-dev libudev-dev pm-utils

# Packages for building Brick firmwares and Bricklet plugins
sudo apt-get -y install cmake gcc-arm-none-eabi

# Packages for hardware development (schematic, layout, case design)
sudo apt-get -y install kicad freecad

# Clone all necessary gits
gitgetter=$(mktemp)

cat > ${gitgetter} <<- EOF
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json

page = 1
repos = []
names = []

while True:
    request = urllib2.urlopen('https://api.github.com/orgs/Tinkerforge/repos?page={0}&per_page=100'.format(page))
    data = request.read()
    decoded = json.loads(data)
    repos += decoded

    if len(decoded) < 100:
        break

    page += 1

for repo in repos:
    name = repo['name'].replace('Tinkerforge/', '')

    if not name.startswith('red-brick-'):
        names.append(name)

print ' '.join(names)
EOF

chmod +x ${gitgetter}

gits=( $(${gitgetter}) )

rm ${gitgetter}

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

# Install additional pygments lexers
cd ~/tf/doc/pygments-mathematica/
sudo python setup.py install
cd ~/tf/doc/pygments-octave-fixed/
sudo python setup.py install

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
