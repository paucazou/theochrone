#!/bin/zsh
# This script is used to deploy the Theochrone website
source commonpackagerfunctions.sh

fcm.delete_if_exist _deploy_tmp
mkdir _deploy_tmp
cp -r ../programme ./_deploy_tmp

cd _deploy_tmp
rm -r **/.* # deleting all files starting by .
rm -r **/*__pycache__*
rm -r **/*~
cd programme
rm -r gui 
cd web
rm -r help/migrations/

mv ../images/fetes kalendarium/static/ # for the images of saints
mv spill/static/spill kalendarium/static/ 

print Compiling translation files...
django-admin compilemessages
### deprecated ###
#print Please put shtml in the right repertory. Do not forget base widget nor light widget !
#./manage.py shell 
### end deprecated ### 
# changing some lines
line_to_modify='fpath = os.path.abspath(chemin + "/../spill/static/spill") + "/"'
line_modified='fpath = os.path.abspath(chemin + "/static/spill") + "/"'
fcm.modify_lines kalendarium/views.py $line_to_modify $line_to_modify
print "DEBUG = False" >> ./web/settings.py
print "ALLOWED_HOSTS = ['theochrone.fr','www.theochrone.fr','theochrone.ga','www.theochrone.ga']" >> ./web/settings.py

cd ../../ # returning to _deploy_tmp
#scp -P 22 theochrone@ssh-theochrone.alwaysdata.net:/home/theochrone/_twit_auth_fr ./programme/_twit_auth_fr
#scp -P 22 theochrone@ssh-theochrone.alwaysdata.net:/home/theochrone/_twit_auth_en ./programme/_twit_auth_en
rsync -r programme theochrone@ssh-theochrone.alwaysdata.net:22/home/theochrone/ 

cd .. # returning to wip_fetes
rm -r _deploy_tmp
