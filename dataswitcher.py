#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module prepares the data in xml files
and push them into programme/data folder as pickle files"""

import copy
import enc
import os
import pickle
import programme.officia as officia
import programme.splitter as splitter
import re
import readline

logger = enc.logger
xml_folder = "theoXML/"
xml_files = [] # a list of all the files in xml
file_pattern = re.compile('^[^\.]+.xml$')
for file_name in os.listdir(xml_folder):
    if file_pattern.match(file_name):
        xml_files.append(xml_folder + file_name)

def CompileRegex(objet):
    """Fonction de compilation des regex""" # énormément d'erreurs dans cette fonction = certaines regex font n'importe quoi, et certains titres ne sont pas supprimés.
    
    vaisseau = copy.deepcopy(objet.regex_)
    titres = ['saint([^e]|$|\.|\?)', 'sainte', 'saints','saintes','bienheureux', 'bienheureuse([^s]|$|\.|\?)','bienheureuses.',
              'lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche','janvier','février','mars','avril','mai$', 'juin','juillet','août','septembre','octobre','novembre','décembre',]
    syntaxiques=['de','à','l','le','d','des','du'] #ne pas mettre des mots qui pourraient se trouver dans les annexes : du, après, à,l'
    chiffres = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',]

    annexes = [] # Il faudrait quelque chose de ce genre pour les jours de la semaine, et les données modifiables peut-être lancer la recherche directement depuis la fonction de traitement des données : oui, une recherche par caractéristiques ; cela ne fait pas doublet, mais permet de faire des recherches approximatives.
    annexes.append(objet._couleur)
    if objet.degre == 5:
        annexes += ['(mémoire|commémoraison)']
        titres.append('privilégiée')
    else:
        annexes.append(str(objet.degre) +'classe')
    if objet.commemoraison_privilegiee > 0:
        annexes += ['(mémoire|commémoraison).*privilégiée']
    if objet.fete_du_Seigneur:
        annexes += ['fêtes?(du)?.*seigneur']
    if objet.temporal:
        annexes.append('temporal')
    else:
        annexes.append('sanctoral')
    if isinstance(objet._temps_liturgique,str):
        annexes.append("temps.*" + re.sub('_','.*',objet._temps_liturgique))
    else:
        for item in objet._temps_liturgique:
            annexes.append("temps.*" + re.sub('_','.*',item))
    if objet.pal:
        annexes.append('pro.*aliquibus.*locis')
    if objet.votive:
        annexes.append('votives')
        
    vaisseau['annexes'] = annexes
        
    
    for liste in vaisseau.values():
        for value in liste:
            for i,a in enumerate(syntaxiques):
                if value == a:
                    del(syntaxiques[i])
            for i, a in enumerate(chiffres): # normalement, cette partie devrait permettre d'exclure seulement les nombres correspondants : 10 n'exclue pas 1 et 0, mais seulement 10, 1 suivi d'une lettre, et 0 précédé d'une lettre.
                if value == a:
                    del(chiffres[i])
                elif a in value:
                    if a == value[0]:
                        chiffres[i] = a + "($|[^" + value[1] + "])"
                    elif a == value[1]:
                        chiffres[i] = "(^|[^" + value[0] + "])" + a # tester si ces nouvelles fonctionnalités marchent.
            for i,a in enumerate(titres):
                if re.findall(a,value):
                    del(titres[i])
    if 'refus_fort' in vaisseau.keys():
        vaisseau['refus_fort'] += chiffres + titres
    else:
        vaisseau['refus_fort'] = chiffres + titres
    if 'refus_faible' in vaisseau.keys():
        vaisseau['refus_faible'] += syntaxiques
    else:
        vaisseau['refus_faible'] = syntaxiques
    delete = []
    for index,liste in vaisseau.items():
        if liste == []:
            delete.append(index)
            continue
        for i,mot in enumerate(liste):
            if len(mot) > 4:
                #traitement du [in]
                mot = re.sub("([ae]?i|u)(n|m)($|[^mnaeiouy])",r"([ae]?i|u)(n|m)\3",mot)
                #traitement du i
                mot = re.sub("(y|i)","(y|i)",mot)
                #traitement du son [o]
                mot = re.sub("(ô|o($|[^nm])|e?au)",r"(o|e?au)\2",mot)
                #traitement du œ
                mot = re.sub('œ',r"(oe|œ)",mot)
                #traitement de [on]
                mot = re.sub('o(m([^m])|n([^n]))',r"o(m|n)\2\3",mot)
                #traitement de lettres finales ; on peut y échapper en mettant un point derrière, par exemple, ou un tréma pour le e.
                mot = re.sub('(([^e])t|[dse])$',r"\1?",mot)
                #traitement du h
                mot = re.sub("(^|[^cp])h",r"\1h?",mot)
                #traitement du type [en]
                mot = re.sub('(ea?|a)(m|n)($|[^mnaeiouy])',r"(ea?|a)(m|n)\3",mot)
                # traitement du type é
                mot = re.sub('(é|è|ê|&|[ea][iy]|(et|er)$|e([sx]|nn)|ë(.))',r"(e|&|[ea][iy]|(et|er))\3\4",mot)
                #traitement du [k]
                mot = re.sub("(c($|[^heiy])|(qu?|k))",r"(c|qu|k)\2",mot)
                #traitement du [s]
                mot = re.sub('((^|[^s])s($|[^aous])|c([eiy]))',r"\2(s|c)\3\4",mot) # pris en compte devant a : ça ne marche pas, à revoir
                #traitement de [e]
                mot = re.sub("(eu|e($|[^ts])($|[^nn]))",r"(eu|e)\2\3",mot)
                #traitement des consonnes doubles
                for lettre in 'bcdfglmnprstv':
                    mot = re.sub(lettre+lettre,lettre+lettre+'?',mot)
            liste[i]=officia.sans_accent(mot)
        vaisseau[index]=tuple(liste)
    for key in delete:
        if vaisseau[key] == []:
            del(vaisseau[key])
    objet.regex = vaisseau
    return objet

def prepare_data(pkl_file_name):
    """Prepares obj to be serialized into pickle file.
    pkl_file_name : str : name of the pickle file, without suffix
    return a list of all the object for requested proper and year.
    Example : prepare_data('romanus_1962')
    What does this function :
    - loads all the objects matching with pkl_file_name
    - prepares regex (call CompileRegex)
    - deletes useless attributes (such as regex_)
    - returns the list. At the end of the list, saturday of the Virgin Mary, and Ferie"""
    obj_list = [] # list which will be returned with all the files
    end_of_list = [] # this is necessary because feria and Virgin Saturday MUST be a the end
    # load
    for xml_file in [elt for elt in xml_files if pkl_file_name in elt ]:
        logger.debug(xml_file)
        with enc.Preferences(xml_file) as file:
            tmp_list = file.prefs
        if 'samedi_ferie' in xml_file:
            end_of_list = tmp_list
        else:
            obj_list += tmp_list
    obj_list += end_of_list
    # compile regex
    logger.info("Compile regex")
    [CompileRegex(obj) for obj in obj_list]
    # delete useless attributes
    logger.info('Delete useless attributes')
    for obj in obj_list:
        delattr(obj,'regex_')    
    return obj_list

def data_pickler(pkl_file_name,obj_list):
    """Save obj_list (list) as pickle file
    pkl_file_name has no suffix"""
    file_path = "programme/data/{}_.pkl".format(pkl_file_name)
    logger.info("Pickling... to {}".format(file_path))
    with open(file_path,'bw') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(obj_list)
    return file_path

def main(**kwargs):
    """What did you think ? It is the main function,
    which calls every other one in this module.
    Unfortunately, it will not give you a coffee.
    """
    if kwargs.get('propers') == 'all':
        propers = ['roman','american','english','welsh','scottish','canadian','brazilian','polish','spanish','portuguese','australian','new-zealander']
    elif 'proper' in kwargs:
        propers = [v for k,v in kwargs.items() if 'proper' in k]
    else:
        propers = ['roman']

    ordo = kwargs.get('ordo','1962')

    for proper in propers:
        pkl_file_name = "{}_{}".format(proper,ordo)
        data_pickler(
            pkl_file_name,
            prepare_data(pkl_file_name)
            )

def modify_in_obj(function,pattern='.*',auto_saved=False):
    """This function applies function
    to every file matching pattern.
    If pattern == '.*' (default) : every file
    function is a custom function which takes
    one parameter : a Feast like object
    auto_saved : if True, objects are saved in their
    own file just after function has called the whole file"""
    list_of_files = [file for file in xml_files if re.match(pattern,file) ]
    for file in list_of_files:
        logger.debug(file)
        with enc.Preferences(file,'r') as f:
            list_of_obj = f.prefs
        for obj in list_of_obj:
            function(obj)
        if auto_saved:
            with enc.Preferences(file,'w') as f:
                f.prefs = list_of_obj
                
def finput(prompt='>>> ', text=''):
    text = str(text)
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt + '\n')
    readline.set_pre_input_hook()
    return result

def xml_to_pkl(name):
    """Takes an xml file and convert it to pickle file.
    Input must be a name without suffix, which exists in the theoXML folder
    Put the output to data folder"""
    path = os.path.dirname(enc.__file__) + '/'
    with enc.Preferences(path + 'theoXML/' + name + '.xml','r') as f:
        data = f.prefs
    with open(path + 'programme/data/' + name + '.pkl','bw') as f:
        pickle.Pickler(f).dump(data)
    
def to_dic_word_frequency(name):
    """Loads an xml file name, without suffix)
    which is {word:word_frequency}
    Builds a tuple(words,{word:wordcost},maxword)
    Save it as a pkl file"""
    path = os.path.dirname(enc.__file__) + '/'
    with enc.Preferences(path + 'theoXML/' + name + '.xml','r') as f:
        data = f.prefs
    if not isinstance(data,dict):
        raise ValueError("Please enter a dict")
    data = splitter.build_cost_dic(data)
    with open(path + 'programme/data/' + name + '.pkl','bw') as f:
        pickle.Pickler(f).dump(data)
    
logger.warning(
    """
    Hello ! I'm the logger. I'm pretty useless,
    but I love to print weird things on the screen.
    If you can read that, that means that the module
    is completely loaded, which is a good thing.
    If you want to silent me, please just type :
    dataswitcher.logger.disabled = True
    Happy pickling !""")
