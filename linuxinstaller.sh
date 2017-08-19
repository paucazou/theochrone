#!/bin/zsh

# functions
miss_exit () {
    print $1 was modified. Please check the script before restart.
    exit 1
    }

# delete dist if exists
if [[ -a dist ]] ; then rm -r dist ; fi
if [[ -a tmp ]] ; then rm -r tmp ; fi
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

#check some lines ; if lines were modified, stop the script
## theochrone.pyw
theochrone=$(<$progdir/theochrone.pyw)
line_theochrone0="import shiptobrowser"
line_theochrone1="if args.navigateur:
    if mois_seul:
        sys.exit(shiptobrowser.openBrowser(search_type='month',date=debut))
    elif args.INVERSE != 1:
        sys.exit(shiptobrowser.openBrowser(search_type='reverse',date=debut,keywords=args.INVERSE))
    elif not semaine_seule and not mois_seul and not annee_seule and args.DEPUIS == 1 and args.JUSQUE == 1:
        sys.exit(shiptobrowser.openBrowser(search_type='day',date=debut))
    else:
        sys.exit(shiptobrowser.openBrowser())
el"
if [[ $theochrone != *$line_theochrone0*$line_theochrone1* ]]; then miss_exit $progdir/theochrone.pyw ; else
theochrone=${theochrone/$line_theochrone1/''}
theochrone=${theochrone/$line_theochrone0/''}
print $theochrone > $progdir/theochrone.pyw; fi
## command_line.py
command_line=$(<$progdir/command_line.py)
line_command_line1="'navigateur': {
            'short':['-b'],
            'long':['--browser'],
            },"
line_command_line2='system.add_argument("-b","--browser",dest="navigateur",help=_("""Open Theochrone in your default webbrowser. You can pass args but following options are disabled :
        - --from/--to options
        - a complete week
        - a complete year
        - years before 1960, after 2100
        - every print option.
        If one of the previous args was entered, it will not result an error,
        but the program will use default value."""),action="store_true")'
if [[ $command_line != *$line_command_line1*$line_command_line2* ]]; then miss_exit $progdir/command_line.py ; else
command_line=${command_line/$line_command_line1/''}
command_line=${command_line/$line_command_line2/''}
print $command_line > $progdir/command_line.py; fi

# add some prod lines
print "for value in loggers.values(): value.setLevel(levels[0])" >> $progdir/phlog.py # disable logs
print "import imagines" >> $progdir/theochrone.pyw # import imagines

#pyinstaller
pyinstaller $progdir/theochrone.pyw \
	--name $name \
	$output \
	--paths $progdir:$progdir/gui/ \
	--add-binary $progdir/data/:./data/ \
	--add-binary $progdir/i18n/:./i18n/ \
	--add-binary $progdir/gui/icons/:./gui/icons/ \
	--clean 

pyinstaller $name.spec
mv dist ..
cd ..
rm -r $dir # deleted temp files
exit 0
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
