import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtGraphicalEffects 1.12
import "../."

GamePage {
    id: pageCalendar

    Item {
        id: calendarContainer
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.height > parent.width ? parent.right : undefined
        anchors.bottom: parent.height > parent.width ? undefined : parent.bottom
        height: parent.height > parent.width ? parent.height / 2 : (parent.height - (60-7))/*TitleBar measure - gradient measure : CHANGER VIA GameSettings.fieldHeight*/
        width: parent.height > parent.width ? parent.width : parent.width / 2
        layer.enabled: true

        Calendar {
            id: calendar
            anchors.fill: parent

            style: CalendarStyle {
                gridVisible: false
                gridColor: "white"

                navigationBar: Rectangle{
                    height: GameSettings.fieldHeight
                    width: calendarContainer.width

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

                property var dayName: [qsTr("Mon."),qsTr("Tue."),qsTr("Wed."),qsTr("Thu."),qsTr("Fri."),qsTr("Sat."),qsTr("Sun.")]

                dayOfWeekDelegate: Rectangle {
                    height: GameSettings.fieldHeight * 0.5
                    width: calendarContainer.width

                        Label {
                            anchors.centerIn: parent
                            text: dayName[styleData.index]
                            color: "black"
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
                        color: styleData.selected ? "white" : (styleData.visibleMonth ? "#55ACEE" : "#c9c9c9" )
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
        layer.enabled: true

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
                        height: parent.height > parent.width ? parent.width * 0.9 : parent.height * 0.9

                        RectangularGlow {
                            anchors.fill: parent
                            glowRadius: 5
                            spread: 0
                            color: GameSettings.liturgical_white
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
                        height: parent.height > parent.width ? parent.width * 0.9 : parent.height * 0.9

                        RectangularGlow {
                            anchors.fill: parent
                            glowRadius: 5
                            spread: 0
                            color: GameSettings.liturgical_white
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
                    color: "white"
                    Rectangle
                    {
                        anchors.top: parent.top
                        width: parent.width
                        height: 0.5
                        color: GameSettings.liturgical_white
                    }
                    Item {
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height
                        Image{
                            anchors.centerIn: parent
                            width: parent.height * 0.8
                            height: parent.height * 0.8
                            source: "../images/icons/saint_white.png"
                            fillMode: Image.PreserveAspectFit
                        }
                    }
                    Text {
                        id: name1
                        anchors.left: parent.left
                        topPadding: parent.height / 9
                        leftPadding: parent.height + 15
                        font.pixelSize: 18
                        color: "black"
                        text: qsTr("Saint Martin")
                    }
                    Text {
                        anchors.left: parent.left
                        topPadding: parent.height / 2
                        leftPadding: parent.height + 15
                        font.pixelSize: 14
                        color: "#3c3d42"
                        text: qsTr("Bishop and Confessor")
                    }
                    Item{
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height
                        Image{
                            anchors.centerIn: parent
                            width: parent.height * 0.3
                            height: parent.height * 0.3
                            source: mouse1.pressed ? "../images/icons/moins_white.png" : "../images/icons/plus_white.png"
                        }
                    }
                    MouseArea{
                        id: mouse1
                        anchors.fill: parent
                    }
                }

                Rectangle {
                    color: "white"
                    Rectangle
                    {
                        anchors.top: parent.top
                        width: parent.width
                        height: 0.5
                        color: GameSettings.liturgical_red
                    }
                    Item {
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height
                        Image{
                            anchors.centerIn: parent
                            width: parent.height * 0.8
                            height: parent.height * 0.8
                            source: "../images/icons/saint_red.png"
                        }
                    }
                    Text {
                        id: name2
                        anchors.left: parent.left
                        topPadding: parent.height / 9
                        leftPadding: parent.height + 15
                        font.pixelSize: 18
                        color: "black"
                        text: qsTr("Saint Menne")
                    }
                    Text {
                        anchors.left: parent.left
                        topPadding: parent.height / 2
                        leftPadding: parent.height + 15
                        font.pixelSize: 14
                        color: "#3c3d42"
                        text: qsTr("Martyr")
                    }
                    Item{
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        width: parent.height
                        height: parent.height
                        Image{
                            anchors.centerIn: parent
                            width: parent.height * 0.3
                            height: parent.height * 0.3
                            source: mouse2.pressed ? "../images/icons/moins_red.png" : "../images/icons/plus_red.png"
                        }
                    }
                    MouseArea{
                        id: mouse2
                        anchors.fill: parent
                    }
                }
            }
        }
    }
}
