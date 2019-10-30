import QtQuick 2.12
import QtGraphicalEffects 1.12
import QtQuick.Controls 2.5

Rectangle {
    id: headerBar
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.right: parent.right
    property int windowWidth: parent.width
    property int windowHeight: parent.height
    height: windowHeight > windowWidth ? 2*(40 /*GameSettings.fieldHeight*/) : 40//GameSettings.fieldHeight
    //########## ATTENTION REMTTRE HEIGHT GAMESETTINGS
    color: "#55ACEE"

    Item{
        id: titleAppContainer
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: windowHeight > windowWidth ? parent.right : undefined
        width: windowHeight > windowWidth ? parent.width : parent.width / 2
        height: windowHeight > windowWidth ? parent.height / 2 : parent.height//color: "blue"

        Text {
            id: title
            anchors.centerIn: parent
            text: "Theochrone"
            font.pixelSize: 0
            font.bold: true
            color: "black"
        }
    }

    Item{
        id: searchBarContainer
        anchors.top: windowHeight > windowWidth ? titleAppContainer.bottom : parent.top
        anchors.left: windowHeight > windowWidth ? parent.left : titleAppContainer.right
        anchors.right: parent.right
        width: windowHeight > windowWidth ? parent.width : parent.width / 2
        height: windowHeight > windowWidth ? parent.height / 2 : parent.height

        RectangularGlow {
                id: effect
                anchors.fill: backgroundSearch
                glowRadius: 4
                spread: 0.2
                color: "grey"
                cornerRadius: backgroundSearch.radius + glowRadius
        }

        Rectangle{
            id: backgroundSearch
            anchors.centerIn: parent   //ne change pas les dimensions contrairement à anchors.fill
            width: parent.width * 0.9
            height: parent.height *0.6
            border.width: 1
            border.color: "#00ffffff"
            radius: 5

            Text{
                anchors.centerIn: parent
                text: qsTr("Search")
                color: "grey"
            }
        }
    }
}
