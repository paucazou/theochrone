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
        anchors.bottom: parent.height > parent.width ? undefined : parent.bottom
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



    Item {
        id: festContainer
        anchors.top: parent.height > parent.width ? calendarContainer.bottom : parent.top
        anchors.right: parent.right
        anchors.left: parent.height > parent.width ? parent.left : calendarContainer.right
        anchors.bottom: parent.bottom

        Rectangle {
            id: swipeFestContainer
            width: parent.width
            height: parent.height - GameSettings.fieldHeight
            color: "white"


            SwipeView{
                id: swipeFest
                anchors.centerIn: parent
                width: parent.width * 0.6
                height: parent.height
                currentIndex: swipeNameFest.currentIndex

                Item{
                    id: firstElement
                    Rectangle{
                        anchors.centerIn: parent
                        width: img1.width
                        height: parent.height > parent.width ? parent.width * 0.8 : parent.height * 0.8

                        RectangularGlow {
                            anchors.fill: parent
                            glowRadius: 10
                            spread: 0
                            color: "#c7c7c7"
                            cornerRadius: 0
                        }
                        Image{
                            id: img1
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                            height: parent.height
                            source: "../images/Martin.jpg"
                            antialiasing: true
                        }
                    }
                }
                Item{
                    id: secondElement
                    Rectangle{
                        anchors.centerIn: parent
                        width: img2.width
                        height: parent.height > parent.width ? parent.width * 0.8 : parent.height * 0.8

                        RectangularGlow {
                            anchors.fill: parent
                            glowRadius: 10
                            spread: 0
                            color: "#c7c7c7"
                            cornerRadius: 0
                        }
                        Image{
                            id: img2
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                            height: parent.height
                            source: "../images/Menne.jpg"
                            antialiasing: true
                        }
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
                    color: "#55ACEE"
                    Text {
                        id: name1
                        anchors.centerIn: parent
                        font.pixelSize: 20
                        color: "white"
                        text: qsTr("Saint Martin, Bishop and Confessor")
                    }
                    Rectangle{
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height
                        color: "#55ACEE"
                        Image{
                            anchors.centerIn: parent
                            width: parent.height * 0.3
                            height: parent.height * 0.3
                            source: mouse1.pressed ? "../images/icons/moins.png" : "../images/icons/plus.png"
                        }
                    }
                    MouseArea{
                        id: mouse1
                        anchors.fill: parent
                    }
                }

                Rectangle {
                    color: "#55ACEE"
                    Text {
                        id: name2
                        anchors.centerIn: parent
                        font.pixelSize: 20
                        color: "white"
                        text: qsTr("Saint Menne, Martyr")
                    }
                    Rectangle{
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height
                        color: "#55ACEE"
                        Image{
                            anchors.centerIn: parent
                            width: parent.height * 0.3
                            height: parent.height * 0.3
                            source: mouse2.pressed ? "../images/icons/moins.png" : "../images/icons/plus.png"
                        }
                    }
                    MouseArea{
                        id: mouse2
                        anchors.fill: parent
                    }
                }
            }
        }
        Rectangle{
            id: borderGradient
            anchors.bottom: nameFestContainer.top
            width: parent.width
            height: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#00ffffff" }
                GradientStop { position: 3.0; color: "grey" }
            }
        }
    }
}
