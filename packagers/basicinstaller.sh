#!/bin/sh
#This script installs the theochrone on Unix like platforms
if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagersfunctions.sh
if [[ $USER != root ]; then
	print "It is possible you need to launch this installer as root."
fi

# test python version

check if superior
