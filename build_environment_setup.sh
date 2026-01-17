#/bin/sh

# This script will create a folder named "tf" in your home directory,
# clone all of the tinkerforge gits, install all packages to build,
# the Bindings, the distribution zips, the documentation, Brick firmwares,
# Bricklet plugins, Brick Viewer and Brick Daemon.
# You will also be able to open, view and edit the schematics and layouts
# for Bricks and Bricklets as well as the design files of the cases.

# It was last tested with a Debian Trixie 13.3

cd ~
sudo apt update

# Packages for general use
sudo apt -y install python3 git

# Packages for "generators/generate_all.py"
sudo apt -y install php
sudo apt -y install build-essential mono-complete python3 perl default-jre default-jdk maven nodejs npm php-pear ruby zip golang-go rust-all
sudo npm install -g browserify

# Packages for dotnet (for c# bindings)
wget https://packages.microsoft.com/config/debian/13/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-10.0

# Packages for "generators/test_all.py"
sudo apt -y install libxml2-utils libgd-dev libgd-perl libterm-readkey-perl libb-lint-perl

# Packages for "$:~/doc/ make html"
sudo apt -y install python3-sphinx python3-sphinxcontrib.spelling

# Packages for building and running brickv
sudo apt -y install python3-pyqt5 python3-pyqt5.qtopengl python3-opengl python3-serial python3-setuptools pyqt5-dev-tools

# Packages for building and running brickd
sudo apt -y install pkg-config libusb-1.0-0-dev libudev-dev pm-utils

# Packages for building Brick firmwares and Bricklet plugins
sudo apt -y install cmake gcc-arm-none-eabi

# Packages for hardware development (schematic, layout, case design)
sudo apt -y install kicad freecad

# Clone all necessary gits
gitgetter=$(mktemp)

cat > ${gitgetter} <<- EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import json

page = 1
repos = []
names = []

while True:
    request = urlopen('https://api.github.com/orgs/Tinkerforge/repos?page={0}&per_page=100'.format(page))
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

print(' '.join(names))
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
python3 generate_all.py
python3 copy_all.py

# Install additional pygments lexers
cd ~/tf/doc/pygments-mathematica/
sudo python3 setup.py install
cd ~/tf/doc/pygments-octave-fixed/
sudo python3 setup.py install

# Generate doc
cd ~/tf/doc/
make html

# Generate brickv GUI
cd ~/tf/brickv/src/
python3 build_all_ui.py

# Build brickd
cd ~/tf/brickd/src/
ln -s ../../daemonlib/ .
cd ~/tf/brickd/src/brickd/
make

# To show how it works we set up one Brick for use with kicad and one
# Brick as well as one Bricklet to compile with gcc.


# Build Master Brick
cd ~/tf/master-brick/software/src/
ln -s ../../../bricklib/ .
cd ~/tf/master-brick/software/
make

# Build Temperature Bricklet
cd ~/tf/temperature-bricklet/software/src/
ln -s ../../../bricklib/ .
ln -s ../../../brickletlib/ .
cd ~/tf/temperature-bricklet/software/
make

# Set up hardware design files for Master Brick
cd ~/tf/master-brick/hardware/
ln -s ../../kicad-libraries/ .
# To open schematics and layout:
# kicad ~/tf/master-brick/hardware/master.pro

# Cases can be found in ~/tf/cases and directly opend with freecad. e.g.:
# freecad ~/tf/cases/ambient_light/ambient_light.fcstd

cd ~
echo done
