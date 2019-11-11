import QtQuick 2.12
import QtQml 2.12
import QtGraphicalEffects 1.12
import QtQuick.Controls 2.5

Rectangle {
    id: headerBar
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.right: parent.right
    property int windowWidth: parent.width
    property int windowHeight: parent.height
    height: windowHeight > windowWidth ? 2*(GameSettings.fieldHeight) : GameSettings.fieldHeight
    color: "#55ACEE"

    Item{
        id: titleAppContainer
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: windowHeight > windowWidth ? parent.right : undefined
        width: windowHeight > windowWidth ? parent.width : parent.width / 2
        height: windowHeight > windowWidth ? parent.height / 2 : parent.height//color: "blue"


        Item {
            id: settingsContainer
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            width: parent.height
            height: parent.height

            Rectangle{
                anchors.centerIn: parent
                height: parent.height * 0.6
                width: parent.width * 0.8
                color: mouseMenu.pressed ? "grey" : "#55ACEE"
                border.width: 1
                border.color: "white"
                radius: 5
            }

            Image {
                id: settings
                anchors.centerIn: parent
                width: parent.height * 0.5
                height: parent.width * 0.5
                source: "images/icons/menu.png"

                SequentialAnimation{
                    id: rotation
                    RotationAnimator {
                        target: settings;
                        from: 0
                        to: 180
                        duration: 300
                    }
                }

                MouseArea{
                    id: mouseMenu
                    anchors.fill: parent
                    onClicked:{
                        rotation.running = true
                        drawer.open()
                    }
                }
            }
        }

        Text {
            id: title
            anchors.centerIn: parent
            text: "Theochrone"
            font.pixelSize: 25
            color: "white"
        }
    }

    Item{
        id: searchBarContainer
        anchors.top: windowHeight > windowWidth ? titleAppContainer.bottom : parent.top
        anchors.left: windowHeight > windowWidth ? parent.left : titleAppContainer.right
        anchors.right: parent.right
        width: windowHeight > windowWidth ? parent.width : parent.width / 2
        height: windowHeight > windowWidth ? parent.height / 2 : parent.height


        Rectangle{
            id: backgroundSearch
            anchors.centerIn: parent   //ne change pas les dimensions contrairement à anchors.fill
            width: parent.width - 20
            height: parent.height * 0.60
            color: "white" //Qt.rgba(255, 255, 255, 0.50)
            opacity: 0.5
            radius: parent.width / 2

            Item {
                id: searchContainer
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                width: parent.height
                height: parent.height

                Image {
                    id: searchIcon
                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                    width: parent.width * 0.5
                    height: parent.height * 0.5
                    source: "images/icons/search.png"
                }
            }

            Text{
                anchors.centerIn: parent
                text: qsTr("Search")
                font.pixelSize: 15
                color: "black"
            }
        }
    }
}
