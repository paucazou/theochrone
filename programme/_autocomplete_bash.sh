#!/bin/bash

# This script was made thanks to this page : http://tech.novapost.fr/autocompletion-des-arguments-dans-vos-commandes.html

_theochrone_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
    COMP_CWORD=$COMP_CWORD \
    AUTO_COMPLETE=1 $1 ) )
    }
if [[ $SHELL == /bin/zsh ]] ; then # TODO make a similar thing for fish, etc. 
	autoload bashcompinit ; 
	bashcompinit ; fi
complete -F _theochrone_completion -o default theochrone.py
