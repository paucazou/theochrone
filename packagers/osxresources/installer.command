#!/usr/bin/env zsh
### set colors
autoload -U colors
colors
### cd in the right directory
cd ${0:a:h}

### variables
launcher='theochrone.command'
pyversion=python3.5 # default, may be changed if python3.6 is installed and not python3.5
alias pip='pip3.5' # default, may be chang ed if python3.6 is installed and not python3.5

### Install python itself ?
print Check python3.5...
pypath=`which python3.5`
if [[ $pypath[1] != '/' ]] ; then
	print Python3.5 not found.
	print Check Python3.6...
	pypath=`which python3.6`
	if [[ $pypath[1] != '/' ]]; then
		print Python3.6 not found.	
		print Downloading python3.5...
		pypkg=python3.5.pkg
		curl -o $pypkg -O https://www.python.org/ftp/python/3.5.4/python-3.5.4-macosx10.5.pkg
		print Installing python3.5...
		print ${fg[red]}Please enter your password:
		sudo installer -pkg $pypkg -target /
		if [[ $? != 0 ]]; then
			print Python was not installed. Try again by double-clicking on a file called $pypkg and relaunch this script.
			exit $?
		fi
		rm $pypkg
	else
		print Python3.6 was found and will be used instead of Python3.5
		pyversion=python3.6
		alias pip='pip3.6'
	fi
fi
print Python3.5 was found.

### install libraries
print Updating PIP... # PIP must be upgraded due to the TLS error
pip install pip
print Downloading and installing libraries...
pip install -r requirements.txt

### setting the launcher
print '#!/usr/bin/env zsh \
	dir=${0:a:h} \
	export LC_CTYPE=`defaults read -g AppleLocale`' > $launcher # in case of error, must erase the content of the file
print -n $pyversion >> $launcher
print ' $dir/programme/theochrone.pyw $@ \
	exit $?' >> $launcher
chmod u+x $launcher

### end of script
print The installation is finished. You can remove this file and 'requirements.txt' if you want.
print Thanks for having downloading Theochrone. Please pray for me.
print You can close this window.
exit 0
