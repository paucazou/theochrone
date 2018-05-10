#!/bin/zsh
#This script makes a archive of Theochrone with an installer for Mac OS X users


if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagerfunctions.sh
name=theochrone_osx.zip
# delete if exists
fcm.delete_if_exist dist
fcm.delete_if_exist tmp
fcm.delete_if_exist build

fcm.copy_and_cd

# modify some lines
theochrone=$progdir/theochrone.pyw
fcm.modify_lines $theochrone $pcm_line_theochrone0
fcm.modify_lines $theochrone $pcm_line_theochrone1 $pcm_line_theochrone1_sub

cm=$progdir/command_line.py
fcm.modify_lines $cm $pcm_line_command_line1
fcm.modify_lines $cm $pcm_line_command_line2

# add some prod lines
fcm.add_lines $progdir/phlog.py $pcm_disable_logs
fcm.add_lines $theochrone $pcm_import_imagines

# copy installation files
cp ../osxresources/{installer.command,LISEZ-MOI.txt,README.txt} ./
cp ../../requirements.txt ./

# end of the script
zip -r $name *
mv $name ../outputs/
fcm.end_script
