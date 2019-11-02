import QtQuick 2.12

GamePage {
    anchors.fill: parent

    Rectangle{
        anchors.fill: parent
        color: "red"
        border.color: "black"
        border.width: 10
        Text {
            anchors.centerIn: parent
            text: "Home page"
        }
    }
}
