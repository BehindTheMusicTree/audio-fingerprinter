#!/bin/bash

poolAbsPath=/tmp/audio-fingerprinter/pool/
sudo mkdir -p $poolAbsPath
sudo chmod 775 $poolAbsPath
sudo chown -R $USER $poolAbsPath

logAbsPath=log/
sudo mkdir -p $logAbsPath
sudo chmod 775 $logAbsPath
sudo chown -R $USER $logAbsPath