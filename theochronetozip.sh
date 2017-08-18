#!/bin/zsh
#Script to put the whole program inside a zip archive

if [[ -a tmp ]] ; then rm -r tmp ; fi
mkdir tmp
cp -r programme ./tmp/programme
cp requirement.txt ./tmp
cd tmp
rm -r **/*~
rm -r **/.*
rm -r **/__pycache__
# add some prod lines
print "for value in loggers.values(): value.setLevel(levels[0])" >> programme/phlog.py # disable logs


zip -r theochrone.zip programme 
zip -r theochrone.zip requirement.txt
mv theochrone.zip ..
cd ..
rm -r tmp
exit 0
