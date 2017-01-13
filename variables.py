#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
from sys import argv

priorites={ # classement des priorités dans le missel de 62
    2800:'Noël,Pâques,Pentecôte',
    2700:'Triduum sacrum (jeudi, vendredi et samedi saints',
    2600:'Epiphanie,Ascension,Trinité,Fête-Dieu,Sacré-Cœur, Christ-Roi',
    2500:'Immaculée Conception, Assomption',
    2400:'Vigile et Octave de Noël',
    2300:'Dimanches de l\'Avent, du Carême, de la Passion, dimanche in albis.',
    2200:'Cendres, lundi, mardi, mercredi de la  semaine sainte',
    2100: 'Commémoraison de tous les fidèles défunts', # sauf en cas de dimanche, où il ne vaut que 1499
    2000:'Vigile de la Pentecôte',
    1990:'Jours dans les octaves de Pâques et de la Pentecôte.',
    1900:'Fêtes de première classe de l\'Église universelle non nommées ci-dessus.',
    1800:'Patron principal de la nation',
    1790:'Patron principal de la région, province ecclésiastique ou civile',
    1780:'Patron principal du diocèse',
    1770:'Anniversaire de la dédicace de l\'église cathédrale',
    1760:'Patron principal du lieu, bourg ou cité.',
    1750:'Anniversaire de la dédicace de l\'église propre, de l\'oratoire public ou semi-public qui tient lieu d\'église.',
    1740:'Titulaire de l\'église propre',
    1730:'Titulaire de l\'ordre ou de la congrégation',
    1720:'Fondateur canonisé de l\'ordre ou de la congrégation',
    1710:"Patron principal de l'ordre ou de la congrégation, et de la province religieuse",
    1700:"Fêtes concédées de première classe, mobiles",
    1650:"Fêtes concédées de première classe, fixes",
    # fin de la première classe
    1600:"Fêtes du Seigneur : mobiles",
    1550:"Fêtes du Seigneur : fixes",
    1500:"Dimanches de II ème classe",
    1400:"Fêtes de II ème classe de l'Église universelle qui ne sont pas du Seigneur.",
    1300:"Jours dans l'octave de Noël",
    1200:"Féries de IIème classe : féries de l'Avent du 17 au 23 décembre inclusivement ; féries des Quatre-Temps de l'Avent, du Carême et de septembre",
    1100:"Patron secondaire de la nation",
    1090:"Patron secondaire de la région ou province ecclésiastique ou civile.",
    1080:"Patron secondaire du diocèse",
    1070:"Patron secondaire du lieu, bourg ou cité.",
    1060:"Saints ou Bienheureux mentionnés au n° 43 d",
    1050:"Saints propres à une église n° 45c",
    1040:"Fondateur béatifié de l'ordre ou de la congrégation",
    1030:"Patron secondaire de l'ordre ou de la congrégation, ou de la province religieuse",
    1020:"Saints ou Bienheureux mentionnés au n° 46 e",
    1000:"Fêtes concédées de II ème classe : mobiles",
    950:"Fêtes concédées de II ème classe : fixes",
    900:"Vigiles de IIème classe",
    # fin de la deuxième classe
    800:"Féries du Carême et de la Passion, depuis le jeudi après les cendres jusqu'au samedi avant le deuxième dimanche de la passion inclusivement, hors féries des Quatre-Temps.",
    700:"Saints ou Bienheureux du n°43d",
    680:"Bienheureux propres à une église n° 45 d",
    660:"Saints ou Bienheureux du n°46e",
    640:"Fêtes concédées mobiles",
    620:"Fêtes concédées fixes",
    600:"Fêtes de IIIème classe universelles mobiles.",
    550:"Fêtes de IIIème classe universelles fixes",
    500:"Féries de l'Avent jusqu'au 16 décembre inclusivement, sauf Quatre-Temps",
    400:"Vigiles de IIIème classe.",
    # Fin de la troisième classe
    300:"Office de sainte Marie le samedi",
    200:"Féries de IVème classe",
    #Fin de la quatrième classe
    100:"commémoraisons",
    }

priorites_de_commemoraison={ # Priorités de commémoraisons dans le missel de 62
    100:'dimanche',
    90:'jour liturgique de première classe',
    80:'jours dans l\'octave de Noël',
    70:"féries des Quatre-Temps de septembre",
    60:"féries de l'Avent, du Carême et de la Passion",
    50:"Litanies majeures (uniquement à la messe)",
    0:'commémoraison ordinaire',
    -1:'pas de commémoraison',
    }

derniers_dimanches_apres_pentecote = [
    ['Nombre de jours entre Pâques et le quatrième dimanche de l\'Avent','Vingt-troisième','Troisième restant','Quatrième restant','Cinquième restant','Sixième restant','Vingt-quatrième'],
    [238,0,0,0,0,0,210],
    [245,210,0,0,0,0,217],
    [252,210,217,0,0,0,224],
    [259,210,217,224,0,0,231],
    [266,210,217,224,231,0,238],
    [273,210,217,224,231,238,245]
    ]

codes_erreurs = {
    0 : 'Système',
    1 : 'date',
    2 : 'date',
    3 : '',
    4 : '',
    5 : '',
    6 : '',
    7 : '',
    8 : '',
    9 : '',
    }

temps_liturgiques = {
    'avent' : 'Temps de l\'Avent',
        'nativite' : 'Temps de la Nativité', # tps de Noël
        'epiphanie' : "Temps de l'Épiphanie", # tps de Noël
    'apres_epiphanie':"Temps après l'Épiphanie",
    'septuagesime' : "Temps de la Septuagésime",
        'careme':'Carême proprement dit', # temps du Carême
        'passion':'Temps de la Passion', # temps du Carême
        'paques':"Temps de Pâques", # temps Pascal
        'ascension':"Temps de l'Ascension", # temps Pascal
        'octave_pentecote':"Octave de la Pentecôte", # temps Pascal
    'pentecote':'Temps après la Pentecôte',
    }
    
    
