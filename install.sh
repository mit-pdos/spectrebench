#!/bin/bash

sudo apt-add-repository multiverse
sudo apt-get update
sudo apt-get install -y python-is-python3 python3-selenium python3-numpy firefox git libtbb-dev m4 vagrant virtualbox

sudo usermod -a -G kvm ubuntu

