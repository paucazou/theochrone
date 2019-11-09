import QtQuick 2.0

Rectangle {
    id: festContainer
    width: parent.width
    height: parent.height

    color: "red"
    signal titleClicked(int height)
    onTitleClicked: {
        if(height == 40)
        {
            heightChange[index] = 200
        }
        else
        {
            heightChange[index] = 40
        }
        console.log("heightChange[",index,"] = ",heightChange[index])
    }

    Item {
        id: titleFest
        width: parent.width * 0.9
        height: 40

        Rectangle{
            width: parent.width
            height: parent.height
            color: "#55ACEE"
            border.width: 3
            border.color: "black"

            Text {
                anchors.centerIn: parent
                text: "Fest"
            }
        }

        MouseArea{
            anchors.fill: parent
            onClicked: titleClicked(heightChange[index])
        }
    }

    Item {
        id: tree
        anchors.top: titleFest.top
        visible: heightChange[index] == 40 ? false : true
        width: parent.width - 10
        height: heightChange[index] + 40

        Rectangle{
            width: parent.width
            height: parent.height
            color: "yellow"

            Text {
                anchors.centerIn: parent
                text: "Display info about the fest"
            }
        }
    }
}
