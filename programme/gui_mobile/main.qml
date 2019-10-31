import QtQuick 2.12
import QtQuick.Window 2.12
import "."

Window {
    id: wroot
    visible: true
    width: 720 * .7
    height: 1240 * .7

    Loader{                                           //Charge une sous-page, ici le document SplashScreen.qml
        id: splashLoader
        anchors.fill: parent                          //La page remplit l'écran
        visible: true
        source: "SplashScreen.qml"
        asynchronous: false                           //Affichage dès que la page est entièrement chargé (écrire true pour activé)

        onStatusChanged: {
            if (status === Loader.Ready) {            //Chargement complet de SplashScreen => chargement fichier source pour appLoader
                appLoader.setSource("App.qml");
            }
        }
    }

    Connections{
        target: splashLoader.item
        onReadyToGo: {
            splashLoader.visible = false                //spalshLoader devient invisible
            splashLoader.setSource("")                  //déchargement de splashLoader
            appLoader.visible = true                    //appLoader devient visible
            appLoader.item.init()
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

