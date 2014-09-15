#! /bin/bash

# Install pip
apt-get -y install pip

# Install python deps
pip install -r ./requirements.txt

# Install ghostscript, unoconv
apt-get -y install ghostscript
apt-get -y install unoconv
