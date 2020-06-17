import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12

Page {
    id: settingsPage
    title: qsTr("Paramètres")

    property int maxWidth: 500
    property int contentPadding: 20

    ScrollView{
        anchors.fill: parent
        ColumnLayout{
            anchors.fill: parent
            spacing: 0
            height:  languageDefaultCont.height + 5 + properDefault.height + 5 + history.height
            Rectangle{
                id: languageDefaultCont
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: 110
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Langue par défaut")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                    }
                    ComboBox{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        model: ["Français","English"]
                    }
                }
            }
            Rectangle{
                id: firstSeparateLine
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignHCenter
                height: 5
                Rectangle{
                    anchors.centerIn: parent
                    width: parent.width - 2 * contentPadding
                    height: 0.5
                    color: "#DCDCDC"
                }
            }
            Rectangle{
                id: properDefault
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: 110
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Langue par défaut")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                    }
                    ComboBox{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        model: ["2019","2020","2021"]
                    }
                }
            }
            Rectangle{
                id: secondSeparateLine
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignHCenter
                height: 5
                Rectangle{
                    anchors.centerIn: parent
                    width: parent.width - 2 * contentPadding
                    height: 0.5
                    color: "#DCDCDC"
                }
            }
            Rectangle{
                id: history
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: 110
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Historique")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                    }
                    Text {
                        text: qsTr("Nombre maximum de ligne d'historique")
                        color: "#181818"
                        font.pixelSize: 15
                    }
                    SpinBox{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        from: 0
                        value: 1000
                        to: 10000
                        editable: true
                    }
                }
            }
        }
    }
}
