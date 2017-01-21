Theochrone is a python3 script which offers many tools about liturgical year
in the Roman Rite in the extraordinary form (also called Old Rite, Saint Pius
V Rite, Traditional Latin Mass, etc.)
His main features are : print the feasts celebrated at the date entered by
user, or print the date of the feast entered by user. Other features can be
seen by typing ./theochrone -h .
Theochrone is now a command-line script, but I hope to soon implement a GUI.
Files :
programme : main folder of the program :
	theochrone : main script
	adjutoria : main module, with functions and classes
	other files in it : data made with Pickle.
Dossiers d'objets : folder containing xml data, for developing purpose.
caisse.py : script made to create data used by Theochrone
variables : miscellaneous informations, mainly used by caisse.py
