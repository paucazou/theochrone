import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12

Item {
    anchors.fill: parent

    PathView {
        id: pathView
        currentIndex: swipeNameSaint.currentIndex
        anchors{
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: containerNameSaint.top
        }
        clip: true
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

            function onChangeSignal() {
                model.clear()
                for(var i = 0; i < feast.getNbElements(); i++){
                    model.append(feast.getData(i))
                }
            }
        }
        flickDeceleration: 2000
        highlightRangeMode: PathView.StrictlyEnforceRange
        preferredHighlightBegin: 0.5
        preferredHighlightEnd: 0.5
        pathItemCount: 3

        property real centerX: width / 2
        property real vertOff: height / 2
        property real picSize: height * 0.7

        path: CoverFlowPath {
            pathView: pathView
        }
        delegate: CoverFlowDelegate {}
    }

    Rectangle{
        id: containerNameSaint
        anchors{
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        height: 60
        Rectangle{
            id: topLine
            anchors.top: parent.top
            width: parent.width
            height: 0.5
            color: "#DCDCDC"
        }
        SwipeView{
            id: swipeNameSaint
            currentIndex: pathView.currentIndex
            anchors{
                top: topLine.bottom
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }
            Repeater{
                model: model
                Loader{
                    active: SwipeView.isCurrentItem || SwipeView.isNextItem || SwipeView.isPreviousItem
                    sourceComponent: RowLayout {
                        anchors.fill: parent
                        spacing: 0
                        Rectangle {
                            Layout.preferredWidth: parent.height
                            Layout.minimumHeight: parent.height
                            Layout.fillWidth: true
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
                            Layout.preferredWidth: parent.width - (2 * parent.height)
                            Layout.minimumHeight: parent.height
                            Layout.fillWidth: true
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
                                    anchors.horizontalCenter: parent.horizontalCenter
                                }
                                Text {
                                    id: typeSaint
                                    text: typeFest
                                    color: "#181818"
                                    font.pixelSize: 15
                                    anchors.bottom: parent.bottom
                                    anchors.horizontalCenter: parent.horizontalCenter
                                }
                            }
                        }
                        Rectangle {
                            Layout.preferredWidth: parent.height
                            Layout.minimumHeight: parent.height
                            Layout.fillWidth: true
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
                    }
                }
            }

        }

        MouseArea{
            anchors.fill: parent
            onClicked: {
                stackView.push("qrc:/qml/SaintInfoPage.qml");
                stackView.currentItem.myFirstCurrentIndex = swipeNameSaint.currentIndex;
            }
        }
    }
}
