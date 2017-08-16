#!/bin/zsh
if [[ $1 == *file* ]] ; then
	output="--onefile"
else
	output="--onedir"
fi

pyinstaller programme/theochrone.pyw \
	programme/navette_navigateur.py \
	--name theochrone \
	$output \
	--paths programme/:programme/gui/:programme/web/ \
	--add-binary data/:./ \
	--add-binary i18n/:./ \
	--clean 

pyinstaller theochrone.spec
rm -r build/ theochrone.spec

