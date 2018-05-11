#!/bin/zsh
#Script to put the whole program inside a zip archive

if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagerfunctions.sh

output=theochrone.zip

fcm.delete_if_exist tmp
fcm.delete_if_exist outputs/$output
mkdir tmp
cp -r ../programme ./tmp/programme
fcm.delete_if_exist ./tmp/programme/web/spill/shtml
cp ../requirements.txt ./tmp
cp basicinstaller.sh ./tmp
cd tmp
rm -r **/*~
rm -r **/.*
rm -r **/__pycache__
# add some prod lines
fcm.add_lines $progdir/phlog.py $pcm_disable_logs


zip -r theochrone.zip programme 
zip -r theochrone.zip requirements.txt
#zip -r theochrone.zip basicinstaller.sh # basicinstaller not ready
mv theochrone.zip ../outputs/
cd ..
rm -r tmp
exit 0
