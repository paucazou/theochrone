#!/usr/local/bin/zsh
#This script makes a Theochrone standalone for OS X with py2app
# WARNING this script was made based on manual work in command line and was not tested


if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagerfunctions.sh
args=()
# delete if exists
fcm.delete_if_exist dist
fcm.delete_if_exist tmp
fcm.delete_if_exist build

# parameters
if [[ $1 == *32* ]] ; then # 32 bits or 64 bits (default), maybe useless
	name=Theochrone32.zip
	args+='--prefer-ppc'
	
else
	name=Theochrone64.zip
fi

fcm.copy_and_cd
cp ../setup.py ./

# move files and folders
mv $progdir/gui/* $progdir/
theochrone=$progdir/theochrone.py
mv $progdir/theochrone.pyw $theochrone
fcm.modify_lines $theochrone $pcm_line_theochrone0
fcm.modify_lines $theochrone $pcm_line_theochrone1 $pcm_line_theochrone1_sub
dcm.modify_lines $theochrone "from messages import args" "from messages import args
args.langue = 'francais'" 
dcm.modify_lines $theochrone "from gui import main_window" "import main_window"

fcm.modify_lines $progdir/main_window.py "os.chdir(chemin)"
fcm.modify_lines $progdir/settings.py "os.chdir(chemin)"

cm=$progdir/command_line.py
fcm.modify_lines $cm $pcm_line_command_line1
fcm.modify_lines $cm $pcm_line_command_line2

# add some prod lines
fcm.add_lines $progdir/phlog.py $pcm_disable_logs
fcm.add_lines $progdir/theochrone.pyw $pcm_import_imagines

# py2app
python3.5 setup.py py2app $args

# end of the script
mv dist/* ../outputs/
cd ../outputs
zip -r $name theochrone.app
#adding a launcher ?
# ln -s ./theochrone.app/Contents/MacOS/theochrone ./'Theochrone launcher'
# zip -r $name 'Theochrone launcher'
rm -r theochrone.app
fcm.end_script
