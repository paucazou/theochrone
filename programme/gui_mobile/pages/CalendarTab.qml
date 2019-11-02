import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4

GamePage {

    Item {
        id: calendarContainer
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.height > parent.width ? parent.right : undefined
        height: parent.height > parent.width ? parent.height / 2 : (parent.height - (60-7))/*TitleBar measure - gradient measure : CHANGER VIA GameSettings.fieldHeight*/
        width: parent.height > parent.width ? parent.width : parent.width / 2

        Calendar {
            anchors.fill: parent
            minimumDate: new Date(2019, 0, 1)
            maximumDate: new Date(3000, 0, 1)
        }

        //for test zone put Item=>Rectangle
        /*
        color: "red"
        border.color: "blue"
        border.width: 5
        */
    }

    Item {
        id: selectDayContainer
        anchors.top: parent.height > parent.width ? calendarContainer.bottom : parent.top
        anchors.right: parent.right
        anchors.left: parent.height > parent.width ? parent.left : calendarContainer.right
        anchors.bottom: parent.bottom
        //for test zone put Item=>Rectangle
        /*
        color: "blue"
        border.color: "black"
        border.width: 5
        */


        ListModel {
            id: contactModel

            ListElement {
                fest: "Fest of the day 1"
            }

            ListElement {
                fest: "Fest of the day 2"
            }
        }

        Component {
            id: contactDelegate
            Rectangle {
                width: parent.width
                height: 50
                color: "#55ACEE"
                border.width: 5
                border.color: "white"
                Column {
                    anchors.centerIn: parent
                    Text {
                        text: fest
                    }
                }
            }
        }

        ListView {
            anchors.fill: parent
            model: contactModel
            delegate: contactDelegate
            highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
            focus: true
        }
    }
}
