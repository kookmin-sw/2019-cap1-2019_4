#!/bin/bash

# after install home brew, install python2
brew install python@2

#if you want to install python3 
# brew install python

#install aws-cli
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

aws --version
