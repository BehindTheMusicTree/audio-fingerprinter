#!/bin/bash

poolAbsPath=/tmp/bodzify-audio-fingerprinter/pool/
sudo mkdir -p $poolAbsPath
sudo chmod 775 $poolAbsPath
sudo chown -R $USER $poolAbsPath