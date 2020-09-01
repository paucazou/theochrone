import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.15


Item {
    anchors.fill: parent

    // MAJ data
    Connections {
        target: feast

        function onChangeSignal() {
            model.clear()
            for(var i = 0; i < feast.getNbElements(); i++){
                if (feast.checkPal(i)){
                    model.append(feast.getData(i))
                }
            }
        }
    }


    ListView{
        id: listView
        anchors.fill: parent
        model: ListModel{
            id: model
            Component.onCompleted: {
                for(var i = 0; i < feast.getNbElements(); i++){
                    if (feast.checkPal(i)){
                        model.append(feast.getData(i))
                    }
                }
            }
        }
        delegate: contactDelegate
        clip: true
        focus: true
    }

    Component{
        id: contactDelegate
        Item{
            width: listView.width
            height: 80
            RectangularGlow {
                anchors.fill: element
                glowRadius: 2
                spread: 0
                color: "grey"
                cornerRadius: element.radius
            }
            Rectangle {
                id: element
                width: parent.width - 20
                height: 60
                color: "white"
                radius: 10
                anchors.centerIn: parent
                clip: true
                Rectangle {
                    id: icon
                    width: parent.height
                    height: parent.height
                    radius: 10
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
                    Item{
                        anchors.centerIn: parent
                        width: parent.width * 0.9
                        height: parent.height * 0.7
                        Text {
                            id: nameSaint
                            text: nameFest
                            color: "#181818"
                            fontSizeMode: Text.Fit
                            font.pixelSize: 20
                            minimumPixelSize: 1
                            anchors.top: parent.top
                            anchors.left: parent.left
                            anchors.right: parent.right
                        }
                        Text {
                            id: typeSaint
                            text: typeFest
                            color: "#181818"
                            fontSizeMode: Text.Fit
                            font.pixelSize: 15
                            minimumPixelSize: 1
                            anchors.bottom: parent.bottom
                            anchors.left: parent.left
                            anchors.right: parent.right
                        }
                    }
                }
                Rectangle {
                    id: iconGoTo
                    width: parent.height
                    height: parent.height
                    radius: 10
                    anchors.right: parent.right
                    Image {
                        id: more
                        source: "qrc:/images/icons/round_arrow_forward_ios_black_48.png"
                        anchors.centerIn: parent
                        fillMode: Image.PreserveAspectFit
                        width: parent.height * 0.3
                        height: parent.height * 0.3
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
}
