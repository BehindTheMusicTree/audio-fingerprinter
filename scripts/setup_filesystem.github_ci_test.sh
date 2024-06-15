#!/bin/bash

poolAbsPath=/tmp/bodzify-audio-fingerprinter/pool/
sudo mkdir -p $poolAbsPath
sudo chmod 775 $poolAbsPath
sudo chown -R $USER $poolAbsPath

logRelPath=log/
sudo mkdir -p $logRelPath
sudo chmod 775 $logRelPath
sudo chown -R $USER $logRelPath