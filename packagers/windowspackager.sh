#!/bin/zsh
print You must first specify this : '# -*-coding:Latin-1 -* for Windows !!!!'
# This script creates a windows installer with the help of pynsist
# and installer.cfg
if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagerfunctions.sh

# check command line parameters

if [[ $1 == 32 ]]; then
    bitness=32
else
    bitness=64
fi

# prepare tmp
fcm.delete_if_exist tmp
fcm.copy_and_cd
cfg=installer.cfg
cp ../$cfg ./
cp -r ../../../windows_packages/ ./ # for levenshtein wheels and arrow package

# set bitness
preset_bitness='bitness=64'
fcm.modify_lines $cfg $preset_bitness "bitness=$bitness"

# add lines
fcm.add_lines $progdir/phlog.py $pcm_disable_logs

# modify lines
theochrone=$progdir/theochrone.py
mv $progdir/theochrone.pyw $theochrone
fcm.modify_lines $theochrone $pcm_line_theochrone0
fcm.modify_lines $theochrone $pcm_line_theochrone1 $pcm_line_theochrone1_sub
cm=$progdir/command_line.py
fcm.modify_lines $cm $pcm_line_command_line1
fcm.modify_lines $cm $pcm_line_command_line2

pynsist $cfg

cd build/nsis/
output_file=`ls *.exe`
cd ../../
mv build/nsis/$output_file ../outputs/
print $output_file moved in outputs
cd ../outputs/
zip -r theochrone$bitness.zip $output_file
print $output_file zipped
fcm.end_script


