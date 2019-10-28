import QtQuick 2.12
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

    Item {
        anchors.centerIn: parent
        width: Math.min(parent.height, parent.width)*0.4
        height: Math.min(parent.height, parent.width)*0.4 + 15

        Image{      //Affichage du logo
            id: logo
            anchors.centerIn: parent
            source: "images/logo.png"
            width: Math.min(parent.height, parent.width)*0.8
            height: Math.min(parent.height, parent.width)*0.8
        }

        Text {
            anchors.fill: parent
            text: "Le temps au service de Dieu"
            minimumPixelSize: 2
            fontSizeMode: Text.Fit
            font.pixelSize: 200
            verticalAlignment: Text.AlignBottom
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

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
