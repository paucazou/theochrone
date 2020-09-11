import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.15

Item {
    anchors.fill: parent

    // MAJ data on homeModel
    Connections {
        target: feast

        function onChangeSignal() {
            homeModel.clear()
            for(var i = 0; i < feast.getNbElements(); i++){
                if (feast.checkPal(i)){
                    homeModel.append(feast.getData(i))
                }
            }
        }
    }

    SwipeView{
        id: swipeImageSaint
        currentIndex: swipeNameSaint.currentIndex
        anchors{
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: indicator.top
        }
        clip: true
        Repeater{
            model: ListModel{
                id: homeModel
                Component.onCompleted: {
                    for(var i = 0; i < feast.getNbElements(); i++){
                        if (feast.checkPal(i)){
                            homeModel.append(feast.getData(i))
                        }
                    }
                }
            }
            Loader {
                active: SwipeView.isCurrentItem || SwipeView.isNextItem || SwipeView.isPreviousItem
                sourceComponent: Rectangle {
                    id: rectDelegate
                    anchors.fill: parent
                    color: "transparent"
                    Image {
                        id: saintImage
                        source: srcImgSaint
                        fillMode: Image.PreserveAspectFit
                        width: parent.width > parent.height ? parent.height * 0.9 : parent.width * 0.9
                        height: parent.width > parent.height ? parent.height * 0.9 : parent.width * 0.9
                        anchors.centerIn: parent
                        smooth: true

                        layer.enabled: true
                        layer.effect: OpacityMask {
                            maskSource: Item {
                                width: saintImage.width
                                height: saintImage.height
                                Rectangle {
                                    anchors.centerIn: parent
                                    width: saintImage.paintedWidth
                                    height: saintImage.paintedHeight
                                    radius: 10
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    PageIndicator{
        id: indicator
        currentIndex: swipeImageSaint.currentIndex
        count: repeater.count
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: containerNameSaint.top
        visible: repeater.count > 1 ? true : false
    }

    Rectangle{
        id: containerNameSaint
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 80
        RectangularGlow {
            anchors.fill: element
            glowRadius: 2
            spread: 0
            color: "grey"
            cornerRadius: element.radius
        }
        Rectangle{
            id: element
            width: parent.width - 20
            height: 60
            color: "white"
            radius: 10
            anchors.centerIn: parent
            clip: true
            SwipeView{
                id: swipeNameSaint
                currentIndex: swipeImageSaint.currentIndex
                anchors.fill: parent
                Repeater{
                    id: repeater
                    model: homeModel
                    Loader{
                        active: SwipeView.isCurrentItem || SwipeView.isNextItem || SwipeView.isPreviousItem
                        sourceComponent: RowLayout {
                            anchors.fill: parent
                            spacing: 0
                            Rectangle {
                                id: icon
                                Layout.preferredWidth: parent.height
                                Layout.minimumHeight: parent.height
                                Layout.fillWidth: true
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
                                Layout.preferredWidth: parent.width - (2 * parent.height)
                                Layout.minimumHeight: parent.height
                                Layout.fillWidth: true
                                Item{
                                    anchors.centerIn: parent
                                    width: parent.width * 0.9
                                    height: parent.height * 0.7
                                    Text {
                                        id: nameSaint
                                        text: nameFest
                                        color: "#181818"
                                        horizontalAlignment: Text.AlignHCenter
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
                                        horizontalAlignment: Text.AlignHCenter
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
                                Layout.preferredWidth: parent.height
                                Layout.minimumHeight: parent.height
                                Layout.fillWidth: true
                                radius: 10
                                Image {
                                    id: more
                                    source: "qrc:/images/icons/round_arrow_forward_ios_black_48.png"
                                    anchors.centerIn: parent
                                    fillMode: Image.PreserveAspectFit
                                    width: parent.height * 0.3
                                    height: parent.height * 0.3
                                }
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
