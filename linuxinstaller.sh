#!/bin/zsh

# delete dist if exists
if [[ -a dist ]] ; then rm -r dist ; fi
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
# copy main folder to tmp
dir=tmp
mkdir $dir 
cp -r ./programme/ $dir/
cd $dir
progdir=./programme
# add some prod lines
print "for value in loggers.values(): value.setLevel(levels[0])" >> $progdir/phlog.py # disable logs
print "import imagines" >> $progdir/theochrone.pyw # import imagines

pyinstaller $progdir/theochrone.pyw \
	--name $name \
	$output \
	--paths $progdir:$progdir/gui/:$progdir/web/ \
	--add-binary $progdir/data/:./data/ \
	--add-binary $progdir/i18n/:./i18n/ \
	--add-binary $progdir/gui/icons/:./gui/icons/ \
	#--add-binary $progdir/gui/i18n/*.qm:./gui/i18n/ \
	--clean 

pyinstaller $name.spec
mv dist ..
cd ..
rm -r $dir # deleted temp files

