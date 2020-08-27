import QtQuick 2.12
import QtQuick.Controls 2.5

ListModel{
    id: theModel

    Component.onCompleted: {
        for(var i = 0; i < feast.getNbElements(); i++){
            theModel.append(feast.getData(i))
        }
    }
}

/*
ListModel{  // just for the example
    id: theModel
    ListElement{
        nameFest: "Saint Martin"
        typeFest: "Évêque et Confesseur"
        srcImg: "qrc:/images/icons/saint_gold.png"
        srcImgSaint: "qrc:/images/background/Martin.jpg"

        proper: "Romain"
        edition: "1962"
        celebration: "Cette fête est célébrée."
        classe: "3"
        liturgicalColor: "Blanc"
        temporal: "Non"
        sanctoral: "Oui"
        liturgicalTime: "Temps per Annum après la Pentecôte"
        transferredFest: "Non"
        massText: "http://introibo.fr/11-11-St-Martin-eveque-et"
    }
    ListElement{
        nameFest: "Saint Menne"
        typeFest: "Martyr"
        srcImg: "qrc:/images/icons/saint_red.png"
        srcImgSaint: "qrc:/images/background/Menne.jpg"

        proper: "Romain"
        edition: "1962"
        celebration: "Cette fête est commémorée."
        classe: "Commémoraison"
        liturgicalColor: "Rouge"
        temporal: "Non"
        sanctoral: "Oui"
        liturgicalTime: "Temps per Annum après la Pentecôte"
        transferredFest: "Non"
        massText: "http://introibo.fr/11-11-St-Menne-martyr"
    }
}
*/
