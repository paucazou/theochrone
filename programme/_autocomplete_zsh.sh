#compdef theochrone.py

# Fonctions à mettre ailleurs
fpath=($PWD $fpath)
autoload -Uz compinit ; compinit

_arguments -s \
	'-r[Research by name]' \
	'-m[Larger research]' \

