import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12


Item {
    anchors.fill: parent

    ListView{
        id: listView
        anchors.fill: parent
        model: ListModel{
            id: model
            Component.onCompleted: {
                for(var i = 0; i < feast.getNbElements(); i++){
                    model.append(feast.getData(i))
                }
            }
        }
        Connections {
            target: feast

            onChangeSignal: {
                model.clear()
                for(var i = 0; i < feast.getNbElements(); i++){
                    model.append(feast.getData(i))
                }
            }
        }
        delegate: contactDelegate
        clip: true
        focus: true
        highlight:
            Rectangle{
            id: topLine
            anchors.top: parent.top
            width: parent.width
            height: 0.5
            color: "#DCDCDC"
        }
    }

    Component{
        id: contactDelegate
        Item {
            width: listView.width
            height: 60
            Rectangle {
                id: icon
                width: parent.height
                height: parent.height
                color: "white"
                Image {
                    id: iconXP
                    source: srcImg
                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                    width: parent.height * 0.8
                    height: parent.height * 0.8
                }
            }
            Rectangle {
                id: textContainer
                anchors.top: parent.top
                anchors.left: icon.right
                anchors.bottom: parent.bottom
                anchors.right: iconGoTo.left
                color: "white"
                Item{
                    anchors.centerIn: parent
                    width: parent.width * 0.7
                    height: parent.height * 0.7
                    Text {
                        id: nameSaint
                        text: nameFest
                        color: "#181818"
                        font.pixelSize: 20
                        anchors.top: parent.top
                    }
                    Text {
                        id: typeSaint
                        text: typeFest
                        color: "#181818"
                        font.pixelSize: 15
                        anchors.bottom: parent.bottom
                    }
                }
            }
            Rectangle {
                id: iconGoTo
                width: parent.height
                height: parent.height
                anchors.right: parent.right
                color: "white"
                Image {
                    id: more
                    source: "qrc:/images/icons/round_arrow_forward_ios_black_48.png"
                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                    width: parent.height * 0.5
                    height: parent.height * 0.5
                }
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    listView.currentIndex = index;
                    stackView.push("qrc:/qml/SaintInfoPage.qml");
                    stackView.currentItem.myFirstCurrentIndex = listView.currentIndex;
                }
            }
        }
    }
}
