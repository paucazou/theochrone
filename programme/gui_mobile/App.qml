import QtQuick 2.12
import QtQuick.Controls 2.2

Item {
    id: app
    anchors.fill: parent
    opacity: 0.0


    property var pages: ["pages/CalendarTab.qml",
                         "pages/SettingsTab.qml"]

    property int __currentIndex: 0

    function init()
    {
        opacity = 1.0
    }

    Loader {
        id: pageLoader
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: headerBar.bottom
        anchors.bottom: parent.bottom
        source: "pages/CalendarTab.qml"

        onStatusChanged: {
            if (status === Loader.Ready)
            {
                pageLoader.item.forceActiveFocus()
            }
        }
    }

    HeaderBar{
        id: headerBar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
    }

    Rectangle{
        id: borderGradientHeader
        anchors.top: headerBar.bottom
        width: parent.width
        height: 7
        gradient: Gradient {
                GradientStop { position: 0.0; color: "grey" }
                GradientStop { position: 0.7; color: "#00ffffff" }
        }
    }

    Drawer {
        id: drawer
        width: 300
        height: parent.height
        interactive: true
    }

    transform: Translate {  //translation Drawer when opened
        x: drawer.position * drawer.width
    }

    Keys.onReleased: {  //user interaction to quit
        switch (event.key) {
        case Qt.Key_Escape:
        case Qt.Key_Back: {
            if (__currentIndex > 0) {
                pageLoader.item.close()
                event.accepted = true
            } else {
                Qt.quit()
            }
            break;
        }
        default: break;
        }
    }

}
