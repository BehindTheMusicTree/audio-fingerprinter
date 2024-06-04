#!/bin/bash

appFilesToAnalyseDirAbsPath=/var/audio-fingerprint-generator/pool/
sudo mkdir -p $appFilesToAnalyseDirAbsPath
sudo chmod 775 $appFilesToAnalyseDirAbsPath
sudo chown -R $USER $appFilesToAnalyseDirAbsPath