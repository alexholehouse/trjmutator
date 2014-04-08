#!/bin/bash

## Alex Holehouse
## April 2014
## trjmutator v0.1
## 
## Installation script for trjmutator
##
## Change either INSTALL_DIR or BINARY_LINK to define where you
## want installation to proceed
##
## Script should be run as root, or if you wish to install in
## a non root directory pass the argumet "user" - i.e. 
##
##     bash install.sh user # will run without being root
##
##     bash install         # requires root  
##


###########################################
INSTALL_DIR="/usr/lib/trjmutator"         
BINARY_LINK="/usr/bin/trjmutator"
###########################################



if [ "$UID" -ne 0 ] && [ "$1" -ne "user" ]
  then echo "ERROR: Please run as root"
  exit
fi

echo "--------------------------------------------"
date
echo "Installing code to $INSTALL_DIR"
echo "Installing symbolic link to $BINARY_LINK"
echo "--------------------------------------------"



## Check if an installation exists already - if it does just delete and 
## move on with a fresh installation
if [ -d $INSTALL_DIR ]
then
    echo "Found existing installation - re-installing"
    rm -r $INSTALL_DIR
    rm $BINARY_LINK 2>/dev/null # remove symbolic link too
fi

echo -e "Installing...\c"

mkdir $INSTALL_DIR
cd src
cp PDB.py $INSTALL_DIR

## Here, we use sed to replace the occurrence of "import PDB" 
## with the appropriate path appending of the install location
## and import of PDB. Useful tip - you can pass sed `any` character
## as the sed deliniator (here I use ;) which avoids having to
## escape "/" in the variable. Pretty nifty!

sed -e "s;import PDB;import os, sys\nlib_path = os.path.abspath('$INSTALL_DIR')\nsys.path.append(lib_path)\nimport PDB;" trjmutator > $INSTALL_DIR/trjmutator
chmod 755 $INSTALL_DIR/trjmutator

# create the link
ln -s $INSTALL_DIR/trjmutator $BINARY_LINK

echo "   [DONE]"
echo "--------------------------------------------"
cd ../

echo "Installation complete"
date
