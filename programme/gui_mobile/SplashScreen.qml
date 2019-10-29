import QtQuick 2.12
import QtGraphicalEffects 1.12
import "."

Item {
    id: root
    anchors.fill: parent

    property bool appIsReady: false
    property bool splashIsReady: false

    property bool ready: appIsReady && splashIsReady
    onReadyChanged: if (ready) readyToGo();

    signal readyToGo()

    function appReady()
    {
        appIsReady = true
    }

    Image{
        id: background
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.fill: parent
        fillMode: Image.Tile
        source: "images/background.jpg"
    }

    BrightnessContrast {
            anchors.fill: background
            source: background
            brightness: -0.5
            contrast: 0
        }

    Item {
        id: centralContent
        anchors.centerIn: parent
        width: Math.min(parent.height, parent.width)*0.4
        height: Math.min(parent.height, parent.width)*0.6

       Image{      //Affichage du logo
            id: logo
            anchors.top: centralContent.top
            anchors.horizontalCenter: parent.horizontalCenter
            source: "images/logo.png"
            width: Math.min(parent.height, parent.width)*0.8
            height: Math.min(parent.height, parent.width)*0.8
            asynchronous: true
        }

        Text {
            id: nameApp
            anchors.top: logo.bottom
            anchors.topMargin: 5
            anchors.right: centralContent.right
            anchors.rightMargin: 5
            anchors.left: centralContent.left
            anchors.leftMargin: 5
            text: "Theochrone"
            minimumPixelSize: 3
            fontSizeMode: Text.HorizontalFit
            font.pixelSize:30
            color: "white"
            //verticalAlignment: Text.AlignBottom
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: subNameApp

            anchors.right: centralContent.right
            anchors.rightMargin: 5
            anchors.left: centralContent.left
            anchors.leftMargin: 5
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 5
            text: "Le temps au service de Dieu"
            minimumPixelSize: 2
            fontSizeMode: Text.HorizontalFit
            font.pixelSize:20
            color: "white"
            horizontalAlignment: Text.AlignHCenter
        }
    }


    Timer {
        id: splashTimer
        interval: 1000
        onTriggered: splashIsReady = true
    }

    Component.onCompleted: splashTimer.start()          //Dès que le chargement QML est fini, démarre le Timer
}
