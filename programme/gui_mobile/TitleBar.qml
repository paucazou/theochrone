import QtQuick 2.12

Rectangle    {
    id: titleBar
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.right: parent.right
    height: 60 //GameSettings.fieldHeight #########################!!! ATTENTION REMETTRE APRES
    color: GameSettings.viewColor

    property var __titles: [qsTr("Home"), qsTr("Calendar"), qsTr("Resources"), qsTr("Settings")]
    property var __icons: ["images/icons/house.png",
                           "images/icons/calendar.png",
                           "images/icons/book.png",
                           "images/icons/settings.png"]
    property var __currentIcons: ["images/icons/house_page.png",
                           "images/icons/calendar_page.png",
                           "images/icons/book_page.png",
                           "images/icons/settings_page.png"]

    property int currentIndex: 0

    signal titleClicked(int index)

    Rectangle{
        id: borderGradient
        width: parent.width
        height: 7
        gradient: Gradient {
                GradientStop { position: 0.0; color: "#00ffffff" }
                GradientStop { position: 2.0; color: "grey" }
        }
    }

    Repeater {
        model: 4    //nbr of page

        Item {
            id: container
            x: index * width
            width: titleBar.width / 4
            height: titleBar.height
            anchors.top: borderGradient.bottom
            anchors.bottom: parent.bottom

            Image {
                id: iconDisplay
                anchors.top: container.top
                anchors.topMargin: 5
                anchors.horizontalCenter: parent.horizontalCenter
                source: titleBar.currentIndex === index ? __currentIcons[index] : __icons[index]
                fillMode: Image.PreserveAspectFit
                width: Math.min(parent.height, parent.width)*0.4
                height: Math.min(parent.height, parent.width)*0.4
            }
            Text {
                id: titleDisplay
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 5
                horizontalAlignment: Text.AlignHCenter
                text: __titles[index]
                font.pixelSize: 0
                fontSizeMode: Text.HorizontalFit
                color: titleBar.currentIndex === index ? GameSettings.textColor : GameSettings.disabledTextColor
            }
            MouseArea {     //user action on title bar navigation
                anchors.fill: parent
                onClicked: titleClicked(index)
            }
        }
    }

}
