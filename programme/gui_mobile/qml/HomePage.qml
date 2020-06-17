import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.12


Page {
    id: home

    title: qsTr("Theochrone")

    property bool myCarouselFestView: true
    onMyCarouselFestViewChanged: {
        if (myCarouselFestView == false)
        {
            loaderView.source = "qrc:/qml/ListFestView.qml";
            console.log("Change take effect");
        }
        else
        {
            loaderView.source = "qrc:/qml/CarouselFestView.qml";
        }
    }

    GridLayout{
        id: layoutHomeContainer
        anchors.fill: parent
        columnSpacing: 0
        rowSpacing: 0
        onHeightChanged: {
            if(home.width > home.height)
            {
                layoutHomeContainer.flow = GridLayout.LeftToRight;
            }
            else
            {
                layoutHomeContainer.flow = GridLayout.TopToBottom;
            }
        }

        Rectangle{
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"

            Calendar {
                id: calendar
                anchors.fill: parent

                style: CalendarStyle {
                    gridVisible: false
                    gridColor: "white"

                    navigationBar: Rectangle{
                        height: previousMonth.height
                        width: calendar.width

                        ToolButton{
                            id: previousMonth
                            anchors.left: parent.left
                            height: 50
                            width: 50
                            Image {
                                source: "qrc:/images/icons/round_arrow_back_ios_black_48.png"
                                anchors.centerIn: parent
                                width: parent.height * 0.5
                                height: parent.width * 0.5
                            }
                            onClicked: {
                                calendar.showPreviousMonth();
                            }
                        }

                        Label {
                            text: styleData.title
                            anchors.centerIn: parent
                            font.pixelSize: 20
                            color: "black"
                        }

                        ToolButton{
                            id: nextMonth
                            anchors.right: parent.right
                            height: 50
                            width: 50
                            Image {
                                source: "qrc:/images/icons/round_arrow_forward_ios_black_48.png"
                                anchors.centerIn: parent
                                width: parent.height * 0.5
                                height: parent.width * 0.5
                            }
                            onClicked: {
                                calendar.showNextMonth();
                            }
                        }
                    }

                    property var dayName: [qsTr("LUN"),qsTr("MAR"),qsTr("MER."),qsTr("JEU"),qsTr("VEN"),qsTr("SAM"),qsTr("DIM")]

                    dayOfWeekDelegate: Rectangle {
                        height: 30
                        width: 30
                        Label {
                            anchors.centerIn: parent
                            text: dayName[styleData.index]
                            color: "#939393"
                            font.pixelSize: 10
                        }
                        Rectangle{
                            id: bottomLine
                            anchors.bottom: parent.bottom
                            width: parent.width
                            height: 0.5
                            color: "#DCDCDC"
                        }
                    }

                    dayDelegate: Rectangle {
                        Rectangle{
                            anchors.centerIn: parent
                            width: parent.height > parent.width ? parent.width : parent.height
                            height: parent.height > parent.width ? parent.width : parent.height
                            border.color: styleData.selected ? "#55ACEE" : "white"
                            border.width: 0.5
                            color: "transparent"
                            radius: (parent.height / 2)
                            Rectangle{
                                height: 4
                                width: 4
                                radius: 2
                                anchors.horizontalCenter: parent.horizontalCenter
                                anchors.top: parent.top
                                anchors.topMargin: 3 * (parent.height / 4)
                                color: styleData.selected ? "#55ACEE" : "white"
                            }
                        }

                        Label {
                            text: styleData.date.getDate()
                            anchors.centerIn: parent
                            color: styleData.selected ? "#55ACEE" : (styleData.visibleMonth ? "#181818" : "#C9C9C9" )
                        }
                    }
                }
            }
        }

        Rectangle{
            id: festView
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"

            Loader{
                id: loaderView
                anchors.fill: parent
                source: "qrc:/qml/CarouselFestView.qml"
            }
        }
    }
}
