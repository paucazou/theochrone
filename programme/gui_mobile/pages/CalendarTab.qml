import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtGraphicalEffects 1.12
import "../."

GamePage {

    Item {
        id: calendarContainer
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.height > parent.width ? parent.right : undefined
        height: parent.height > parent.width ? parent.height / 2 : (parent.height - (60-7))/*TitleBar measure - gradient measure : CHANGER VIA GameSettings.fieldHeight*/
        width: parent.height > parent.width ? parent.width : parent.width / 2

        Calendar {
            id: calendar
            anchors.fill: parent

            style: CalendarStyle {
                gridVisible: false

                navigationBar: Rectangle{
                    height: GameSettings.fieldHeight
                    width: calendarContainer.width
                    color: "white"

                    Label {
                        text: styleData.title
                        anchors.centerIn: parent
                        font.bold: true
			font.pixelSize: 15
                        color: "#55ACEE"
                    }

                    Item {
                        id: previous
                        anchors.top: parent.top
                        anchors.left: parent.left
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height

                        Image{
                            id: previousImage
                            anchors.centerIn: parent
                            width: parent.height * 0.4
                            height: parent.width * 0.4
                            source: mousePrevious.pressed ? "../images/icons/back_clicked.png" : "../images/icons/back.png"
                        }
                        MouseArea{
                            id: mousePrevious
                            anchors.fill: parent
                            onClicked: {
                                calendar.showPreviousMonth();
                            }
                        }
                    }

                    Item {
                        id: next
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height

                        Image{
                            id: nextImage
                            anchors.centerIn: parent
                            width: parent.height * 0.4
                            height: parent.width * 0.4
                            source: mouseNext.pressed ? "../images/icons/next_clicked.png" : "../images/icons/next.png"
                        }
                        MouseArea{
                            id: mouseNext
                            anchors.fill: parent
                            onClicked: {
                                calendar.showNextMonth()
                            }
                        }
                    }
                }

                dayDelegate: Rectangle {
                    RadialGradient {
                        anchors.centerIn: parent
                        visible: styleData.selected ? true : false
                        width: parent.height > parent.width ? parent.width : parent.height
                        height: parent.height > parent.width ? parent.width : parent.height

                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "grey" }
                            GradientStop { position: 0.5; color: "white" }
                        }
                    }
                    Rectangle{
                        anchors.centerIn: parent
                        width: parent.height > parent.width ? parent.width * 0.8 : parent.height * 0.8
                        height: parent.height > parent.width ? parent.width * 0.8 : parent.height * 0.8
                        color: styleData.selected ? "#55ACEE" : "white"
                        radius: (parent.height / 2)
                    }

                    Label {
                        text: styleData.date.getDate()
                        anchors.centerIn: parent
                        font.bold: true
                        color: styleData.selected ? "white" : (styleData.visibleMonth ? "#55ACEE" : "grey" )
                    }
                }
            }
        }
    }

    Item {
        id: selectDayContainer
        anchors.top: parent.height > parent.width ? calendarContainer.bottom : parent.top
        anchors.right: parent.right
        anchors.left: parent.height > parent.width ? parent.left : calendarContainer.right
        anchors.bottom: parent.bottom

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
