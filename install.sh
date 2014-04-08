#!/bin/bash

## Installation script for trjmutator
## 
##


###########################################
INSTALL_DIR="/usr/lib/trjmutator"         
BINARY_LINK="/usr/bin/trjmutator"
###########################################

echo "Installing code to $INSTALL_DIR"
echo "Installing symbolic link to $BINARY_LINK"


## Check if an installation exists already - if it does just delete and 
## move on with a fresh installation
if [ -d $INSTALL_DIR ]
then
    echo "Found existing directory - re-installing"
    rm -r $INSTALL_DIR
    rm $BINARY_LINK 2>/dev/null # remove symbolic link too
fi

mkdir $INSTALL_DIR
cd src
cp PDB.py $INSTALL_DIR

## Here, we use sed to replace the occurrence of "import PDB" 
## with the appropriate path appending of the install location
## and import of PDB

sed -e "s;import PDB;import os, sys\nlib_path = os.path.abspath('$INSTALL_DIR')\nsys.path.append(lib_path)\nimport PDB;" trjmutator > $INSTALL_DIR/trjmutator
chmod 755 $INSTALL_DIR/trjmutator


ln -s $INSTALL_DIR/trjmutator $BINARY_LINK

cd ../


echo "Installation complete"
