import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12

Page {
    id: saintInfoPage
    title: qsTr("Résultats")

    property int maxWidth: 500
    property int contentPadding: 20

    property int myFirstCurrentIndex: 0
    onMyFirstCurrentIndexChanged: {
        swipeView.currentIndex = myFirstCurrentIndex;
    }

    SwipeView{
        id: swipeView
        anchors.fill: parent
        Repeater{
            model: ListModelExample{}
            Loader{
                active: SwipeView.isCurrentItem || SwipeView.isNextItem || SwipeView.isPreviousItem
                sourceComponent: ScrollView{
                    anchors.fill: parent
                    ColumnLayout{
                        anchors.fill: parent
                        spacing: 0
                        height:  backgroundSaintCont.height + tableInfoCont.height

                        Rectangle{
                            id: backgroundSaintCont
                            Layout.fillWidth: true
                            Layout.maximumWidth: maxWidth
                            Layout.alignment: Qt.AlignCenter
                            Layout.fillHeight: true
                            Layout.maximumHeight: maxWidth
                            color: "white"
                            height: 250
                            Image {
                                id: backgroundSaintImage
                                source: srcImgSaint != "" ? srcImgSaint : "qrc:/images/background/default_image_saint.png"
                                anchors.centerIn: parent
                                width: parent.height - contentPadding
                                height: parent.height - contentPadding
                                fillMode: Image.PreserveAspectFit
                            }
                        }
                        Rectangle{
                            id: tableInfoCont
                            Layout.fillWidth: true
                            Layout.maximumWidth: maxWidth
                            Layout.alignment: Qt.AlignHCenter
                            Layout.preferredHeight: 600
                            Layout.maximumHeight: 10000
                            Column{
                                id: col
                                anchors.fill: parent
                                anchors.margins: contentPadding
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Propre")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: proper
                                        color: "#333333"
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Édition")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: edition
                                        color: "#333333"
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Célébration")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: celebration
                                        color: "#333333"
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Classe")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: classe
                                        color: "#333333"
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Couleur liturgique")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: liturgicalColor
                                        color: "#333333"
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Temporal")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: temporal
                                        color: "#333333"
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Sanctoral")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: sanctoral
                                        color: "#333333"
                                        width: 2 * parent.width / 3
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Temps liturgique")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: liturgicalTime
                                        color: "#333333"
                                        padding: 15
                                        width: 2 * parent.width / 3
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 1
                                    color: "#DDDDDD"
                                }
                                Row{
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    Text {
                                        text: qsTr("Fête transférée")
                                        width: parent.width / 3
                                        font.bold: true
                                        padding: 15
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                    Text {
                                        text: transferredFest
                                        color: "#333333"
                                        padding: 15
                                        width: 2 * parent.width / 3
                                        clip: true
                                        wrapMode: Text.Wrap
                                    }
                                }
                                Rectangle{
                                    width: parent.width
                                    height: 50
                                    color: "#F5F5F5"
                                    Text {
                                        text: qsTr("Textes de la messe et de l'office sur Intoibo.fr")
                                        color: "#55ACEE"
                                        baseUrl: "https://www.introibo.fr/"
                                        padding: 15
                                        clip: true
                                        height: 40
                                    }
                                    MouseArea{
                                        anchors.fill: parent
                                        onClicked: Qt.openUrlExternally("https://theochrone.fr");
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
