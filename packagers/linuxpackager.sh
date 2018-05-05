#!/bin/zsh
# This script packages the program with the help of pyinstaller
if [[ $PWD != *packagers ]] ; then print Please go to packagers dir ; exit 1 ; fi
source commonpackagerfunctions.sh


# delete dist if exists
fcm.delete_if_exist dist
fcm.delete_if_exist tmp
# parameters
if [[ $1 == *file* ]] ; then # one file or one folder (default)
	output="--onefile"
else
	output="--onedir"
fi
if [[ $2 == *32* ]] ; then # 32 bits or 64 bits (default)
	name=theochrone32
else
	name=theochrone64
fi

fcm.copy_and_cd
# modify some lines
theochrone=$progdir/theochrone.pyw
#mv $progdir/theochrone.pyw $theochrone
fcm.modify_lines $theochrone $pcm_line_theochrone0
fcm.modify_lines $theochrone $pcm_line_theochrone1 $pcm_line_theochrone1_sub
cm=$progdir/command_line.py
fcm.modify_lines $cm $pcm_line_command_line1
fcm.modify_lines $cm $pcm_line_command_line2

# add some prod lines
fcm.add_lines $progdir/phlog.py $pcm_disable_logs
fcm.add_lines $progdir/theochrone.pyw $pcm_import_imagines

#pyinstaller
pyinstaller $progdir/theochrone.pyw \
	--name $name \
	$output \
	--paths $progdir:$progdir/gui/ \
	--add-binary $progdir/data/:./data/ \
	--add-binary $progdir/i18n/:./i18n/ \
	--add-binary $progdir/gui/icons/:./gui/icons/ \
	--add-binary $progdir/gui/i18n/:./gui/i18n/ \
	--clean 

pyinstaller $name.spec
print $PWD
mv dist/* ../outputs/
fcm.end_script

#options disabled

	--hidden-import html.parser \
#--add-binary $progdir/gui/i18n/*.qm:./gui/i18n/ \

	--add-binary $progdir/$statickal/images/:./$statickal/images/ \
	--add-binary $progdir/$statickal/bootstrap/fonts/glyphicons-halflings-regular.eot:./$statickal/bootstrap/fonts/glyphicons-halflings-regular.eot \
	--add-binary $progdir/$statickal/bootstrap/fonts/glyphicons-halflings-regular.ttf:./$statickal/bootstrap/fonts/glyphicons-halflings-regular.ttf \
	--add-binary $progdir/$statickal/bootstrap/fonts/glyphicons-halflings-regular.woff:./$statickal/bootstrap/fonts/glyphicons-halflings-regular.woff \
	--add-binary $progdir/$statickal/fonts/font-awesome/fonts/FontAwesome.otf:./$statickal/fonts/font-awesome/fonts/FontAwesome.otf \
	--add-binary $progdir/$statickal/fonts/font-awesome/fonts/fontawesome-webfont.eot:./$statickal/fonts/font-awesome/fonts/fontawesome-webfont.eot \
	--add-binary $progdir/$statickal/fonts/font-awesome/fonts/fontawesome-webfont.ttf:./$statickal/fonts/font-awesome/fonts/fontawesome-webfont.ttf \
	--add-binary $progdir/$statickal/fonts/font-awesome/fonts/fontawesome-webfont.woff:./$statickal/fonts/font-awesome/fonts/fontawesome-webfont.woff\
	--add-data $progdir/$statickal/bootstrap/fonts/glyphicons-halflings-regular.svg:./$statickal/bootstrap/fonts/glyphicons-halflings-regular.svg \
	--add-data $progdir/$statickal/bootstrap/css:./$statickal/bootstrap/css \
	--add-data $progdir/$statickal/bootstrap/js:./$statickal/bootstrap/js \
	--add-data $progdir/$statickal/css:./$statickal/css \
	--add-data $progdir/$statickal/fonts/font-awesome/css:./$statickal/fonts/font-awesome/css \
	--add-data $progdir/$statickal/fonts/font-awesome/less:./$statickal/fonts/font-awesome/less \
	--add-data $progdir/$statickal/fonts/font-awesome/scss:./$statickal/fonts/font-awesome/scss \
	--add-data $progdir/$statickal/fonts/font-awesome/fonts/fontawesome-webfont.svg:./$statickal/fonts/font-awesome/fonts/fontawesome-webfont.svg \
	--add-data $progdir/$statickal/js:./$statickal/js \
	--add-data $progdir/$statickal/plugins:./$statickal/plugins \
	--add-data $progdir/theoweb/kalendarium/templates/:./theoweb/kalendarium/templates/ \
	
# other things
statickal=theoweb/kalendarium/static/kalendarium
# modify some folder names
mv $progdir/web $progdir/theoweb


ship=$(<$progdir/shiptobrowser.py)
old="path=os.path.dirname(os.path.abspath(__file__))+'/web'"
new="path=os.path.dirname(os.path.abspath(__file__))+'/theoweb'"
print ${ship/$old/$new} > $progdir/shiptobrowser.py
