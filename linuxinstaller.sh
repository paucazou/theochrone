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
# add a python file to copy all the files, check if one of them use a logger, and turn it off ; maybe directly in logger file ?
pyinstaller programme/theochrone.pyw \
	programme/navette_navigateur.py \
	--name $name \
	$output \
	--paths programme/:programme/gui/:programme/web/ \
	--add-binary programme/data/:./data/ \
	--add-binary programme/i18n/:./i18n/ \
	--clean 

pyinstaller $name.spec
rm -r build/ $name.spec # deleted temp files

