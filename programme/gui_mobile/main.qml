import QtQuick 2.12
import QtQuick.Window 2.2
import "."

import StatusBar 0.1
import QtQuick.Controls.Material 2.0

Window {
    id: wroot
    visible: true
    width: 720 * .7
    height: 1240 * .7
    title: "Theochrone"
    color: GameSettings.backgroundColor

    Material.theme: Material.Dark

    StatusBar {
        theme: StatusBar.Dark // or Material.Dark
        color: "#55ACEE"
    }
    /**/

    Component.onCompleted: {
        GameSettings.wWidth = Qt.binding(function() {return width})
        GameSettings.wHeight = Qt.binding(function() {return height})
    }

    Loader{                                           //Charge une sous-page, ici le document SplashScreen.qml
        id: splashLoader
        anchors.fill: parent                          //La page remplit l'écran
        source: "SplashScreen.qml"
        asynchronous: false                           //Affichage dès que la page est entièrement chargé (écrire true pour activé)
        visible: true

        onStatusChanged: {
            if (status === Loader.Ready) {            //Chargement complet de SplashScreen => chargement fichier source pour appLoader
                appLoader.setSource("App.qml");
            }
        }
    }

    Connections{
        target: splashLoader.item
        onReadyToGo: {
            appLoader.visible = true                    //appLoader devient visible
            appLoader.item.init()
            splashLoader.visible = false                //spalshLoader devient invisible
            splashLoader.setSource("");                  //déchargement de splashLoader
        }
    }

    Loader{
        id: appLoader
        anchors.fill: parent
        visible: false
        //source chargé dans Connections
        asynchronous: true
        onStatusChanged: {
            if (status === Loader.Ready)
                splashLoader.item.appReady()
        }
    }

}

