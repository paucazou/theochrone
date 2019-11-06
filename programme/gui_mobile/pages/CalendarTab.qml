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
            id: contactModelTitleFest

            ListElement {
                fest: "Fest of the day 2"
            }

            ListElement {
                fest: "Fest of the day 1"
            }
        }

        Component {
            id: contactTitleFest
            Item {
                id: festContainer
                width: parent.width
                height: 2*40 /* CHANGER par heightField gammesettings */

                signal titleClicked()
                onTitleClicked: {
                    console.log("Click OK")
                }

                Item {
                    id: titleFest
                    anchors.centerIn: parent
                    width: parent.width - 20
                    height: parent.height - 20

                    Rectangle{
                        id: backgroundTitleFest
                        width: parent.width
                        height: parent.height
                        color: "#55ACEE"
                        radius: 10

                        Text {
                            anchors.centerIn: parent
                            text: fest
                        }
                    }

                    MouseArea{
                        anchors.fill: parent
                        onClicked: titleClicked()
                    }
                }
            }
        }

        Rectangle{
            anchors.fill: parent

            ListView{
                anchors.fill: parent
                model: contactModelTitleFest
                delegate: contactTitleFest
                focus: true
            }
        }
    }
}
