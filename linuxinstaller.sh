#!/bin/zsh
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
cp -r programme ./$dir
# add some prod lines
print "for value in loggers.values(): value.setLevel(levels[0])" >> $dir/phlog.py # disable logs

pyinstaller $dir/theochrone.pyw \
	$dir/navette_navigateur.py \
	--name $name \
	$output \
	--paths $dir/:$dir/gui/:$dir/web/ \
	--add-binary $dir/data/:./data/ \
	--add-binary $dir/i18n/:./i18n/ \
	--clean 

pyinstaller $name.spec
rm -r build/ $dir $name.spec # deleted temp files

