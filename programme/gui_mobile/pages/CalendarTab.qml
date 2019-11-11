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

                    //Mouse Bubble Animation
                    Rectangle{
                        id: rect /* test bubble clicked*/

                        radius: height / 2
                        color: "#55ACEE"

                        ParallelAnimation {
                            id: anim
                            NumberAnimation { target: rect; property: "width"; from: 0; to: height * 0.8; duration: 80 }
                            NumberAnimation { target: rect; property: "height"; from: 0; to: height * 0.8; duration: 80 }
                        }

                        SequentialAnimation{
                            id: opacityReduct
                            NumberAnimation {
                                target: rect
                                property: "opacity"
                                from: 0.3
                                to: 0.0
                                duration: 300
                                onFinished: {
                                    rect.width = 0
                                    rect.height = 0
                                }
                            }
                        }
                    }
                    //End Mouse Bubble Animation

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
                            onPressed: {

                                //Enable Mouse Bubble Animation
                                rect.opacity = 0.2
                                rect.anchors.centerIn = previous
                                anim.running = true
                            }
                            onClicked: {
                                calendar.showPreviousMonth()
                                opacityReduct.running = true
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
                            onPressed: {

                                //Enable Mouse Bubble Animation
                                rect.opacity = 0.2
                                rect.anchors.centerIn = next
                                anim.running = true
                            }
                            onClicked: {
                                opacityReduct.running = true
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
                        width: parent.height > parent.width ? parent.width : parent.height
                        height: parent.height > parent.width ? parent.width : parent.height
                        color: styleData.selected ? "#55ACEE" : "white"
                        radius: (parent.height / 2)
                    }

                    Label {
                        text: styleData.date.getDate()
                        anchors.centerIn: parent
                        color: styleData.selected ? "white" : (styleData.visibleMonth ? "#55ACEE" : "grey" )
                    }
                }
            }
        }
    }



    Rectangle {
        id: festContainer
        anchors.top: parent.height > parent.width ? calendarContainer.bottom : parent.top
        anchors.right: parent.right
        anchors.left: parent.height > parent.width ? parent.left : calendarContainer.right
        anchors.bottom: parent.bottom
        color: "#f3e2dd"

        Item {
            id: swipeContainer
            width: parent.width
            height: parent.height - GameSettings.fieldHeight

            SwipeView{
                id: swipeFest
                anchors.centerIn: parent
                width: parent.width * 0.6
                height: parent.height
                currentIndex: swipeNameFest.currentIndex

                Rectangle{
                    id: firstElement
                    color: "red"
                    border.width: 10
                    border.color: "black"
                    Image{
                        anchors.centerIn: parent
                        width: parent.height > parent.width ? parent.width * 0.6 : parent.height * 0.6
                        height: parent.height > parent.width ? parent.width * 0.6 : parent.height * 0.6
                        source: "../images/default.png"
                        antialiasing: true
                    }
                }

                Rectangle{
                    id: secondElement
                    color: "yellow"
                    border.width: 10
                    border.color: "black"
                    Image{
                        anchors.centerIn: parent
                        width: parent.height > parent.width ? parent.width * 0.6 : parent.height * 0.6
                        height: parent.height > parent.width ? parent.width * 0.6 : parent.height * 0.6
                        source: "../images/default.png"
                        antialiasing: true
                    }
                }

                Rectangle{
                    id: thirdElement
                    color: "green"
                    border.width: 10
                    border.color: "black"
                    Image{
                        anchors.centerIn: parent
                        width: parent.height > parent.width ? parent.width * 0.6 : parent.height * 0.6
                        height: parent.height > parent.width ? parent.width * 0.6 : parent.height * 0.6
                        source: "../images/default.png"
                        antialiasing: true
                    }
                }

            }
        }

        Rectangle {
            id: nameFestContainer
            anchors.top: undefined
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            width: parent.width
            height: GameSettings.fieldHeight
            color: "white"

            SwipeView{
                id: swipeNameFest
                anchors.centerIn: parent
                width: parent.width
                height: parent.height
                currentIndex: swipeFest.currentIndex

                Rectangle {
                    color: "red"
                    Text {
                        id: name1
                        anchors.centerIn: parent
                        text: qsTr("Fest of the day 1")
                    }
                }

                Rectangle {
                    color: "yellow"
                    Text {
                        id: name2
                        anchors.centerIn: parent
                        text: qsTr("Fest of the day 2")
                    }
                }

                Rectangle {
                    color: "green"
                    Text {
                        id: name3
                        anchors.centerIn: parent
                        text: qsTr("Fest of the day 3")
                    }
                }
            }
        }

        /*ListModel {
            id: contactModelTitleFest

            ListElement {
                fest: "Fest of the day 1"
                dateFest: ""
            }

            ListElement {
                fest: "Fest of the day 2"
            }
        }

        Component {
            id: contactTitleFest
            Item {
                id: festContainer
                width: parent.width
                height: 2*40

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
                        color: "white"
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
        }*/
    }
}
