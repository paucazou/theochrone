#!/bin/zsh
#Script to put the whole program inside a zip archive

if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagerfunctions.sh

cm.delete_if_exist tmp
mkdir tmp
cp -r ../programme ./tmp/programme
cp requirement.txt ./tmp
cp basicinstaller.sh ./tmp
cd tmp
rm -r **/*~
rm -r **/.*
rm -r **/__pycache__
# add some prod lines
fcm.add_lines $progdir/phlog.py $pcm_disable_logs


zip -r theochrone.zip programme 
zip -r theochrone.zip requirement.txt
zip -r theochrone.zip basicinstaller.sh
mv theochrone.zip ..
cd ..
rm -r tmp
exit 0
