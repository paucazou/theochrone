#!/bin/zsh
# This file contains functions and parameters used by more than one packager (say Windows & Linux)
# all functions must start with 'fcm.', all parameters with 'pcm_'
# Don't forget to source this file before use them


# functions
fcm.miss_exit () {
    # use this if a file was modified and some lines must be changed manually
    # $1 -> name of the script modified
    # $2 -> lines deprecated
    print $1 was modified. Please check the script before restart.
    print Here are the lines modified :
    print '#####################################################################'
    print $2
    print '#####################################################################'
    exit 1
    }
    
fcm.delete_if_exist () {
    # use this to check if a file or dir exists and must be deleted
    # $1 -> file/dir path
    if [[ -a $1 ]] ; then rm -r $1 ; fi
    print $1 deleted
    }
    
fcm.copy_and_cd () {
    # copy programme folder to tmp
    # change directory
    dir=./tmp/
    mkdir $dir
    print $dir created
    cp -r ../programme/ $dir
    print program copied
    cd $dir
    print Change dir $dir
    progdir=./programme
    }
    
fcm.modify_lines () {
    # check if original lines ($2) are present in file ($1 -> path)
    # if they are, change them with new lines ($3)
    # to just delete them, just let $3 empty
    # else, exit the program
    file=$1
    file_data=$(<$file)
    original=$2
    new=$3
    
    if [[ $file_data != *$original* ]]; then fcm.miss_exit $file $original; else
    file_data=${file_data/$original/$new}
    fi
    print $file_data > $file
    print $file modified
    }
    
fcm.add_lines () {
    # add lines ($2) at the end of the file ($1)
    print $1 >> $2
    print Lines added at the bottom of $1
    }
    

# parameters
## lines to delete
pcm_line_theochrone0="import shiptobrowser"
pcm_line_theochrone1="if args.navigateur:
    if mois_seul:
        sys.exit(shiptobrowser.openBrowser(search_type='month',date=debut))
    elif args.INVERSE != 1:
        sys.exit(shiptobrowser.openBrowser(search_type='reverse',date=debut,keywords=args.INVERSE))
    elif not semaine_seule and not mois_seul and not annee_seule and args.DEPUIS == 1 and args.JUSQUE == 1:
        sys.exit(shiptobrowser.openBrowser(search_type='day',date=debut))
    else:
        sys.exit(shiptobrowser.openBrowser())
el"

pcm_line_command_line1="'navigateur': {
            'short':['-b'],
            'long':['--browser'],
            },"
pcm_line_command_line2='system.add_argument("-b","--browser",dest="navigateur",help=_("""Open Theochrone in your default webbrowser. You can pass args but following options are disabled :
        - --from/--to options
        - a complete week
        - a complete year
        - years before 1960, after 2100
        - every print option.
        If one of the previous args was entered, it will not result an error,
        but the program will use default value."""),action="store_true")'
        
## lines to add
pcm_disable_logs="for value in loggers.values(): value.setLevel(levels[0])"
pcm_import_imagines="import imagines"
