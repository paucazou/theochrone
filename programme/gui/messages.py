#!/usr/bin/python3
# -*-coding:Utf-8 -*
"""This file contains every text of the GUI for translation purpose.
Each class or function has her own dict translation.
If some text is used in two different classes or functions,
this text is linked to the more important class or function."""

import gettext
gettext.install('messages','./i18n')

# QMainWindow
main_window = {}
## actions
actions = {}
actions['exit_name'] = _("Exit")
actions['exit_status'] = _("Exit the app")

main_window['actions']= actions

## menus
menus = {}
menus['file'] = _("File")
menus['edit'] = _("Edit")
menus['help'] = _("Help")

main_window['menus'] = menus

