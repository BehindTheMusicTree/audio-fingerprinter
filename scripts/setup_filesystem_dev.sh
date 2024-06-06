#!/bin/bash

appFilesToAnalyseDirAbsPath=/tmp/audio-fingerprint-generator/pool/
sudo mkdir -p $appFilesToAnalyseDirAbsPath
sudo chmod 775 $appFilesToAnalyseDirAbsPath
sudo chown -R $USER $appFilesToAnalyseDirAbsPath