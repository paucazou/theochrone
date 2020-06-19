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
            Rectangle{
                id: languageDefaultCont
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: col1.implicitHeight + 2 * contentPadding
                color: "white"
                Column{
                    id: col1
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: qsTr("Langue par défaut")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    ComboBox{
                        id: cB1
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        model: ["Français","English"]
                        background: Rectangle {
                                implicitWidth: 120
                                implicitHeight: 40
                                border.color: cB1.focus ? "#55ACEE" : "grey"
                                border.width: cB1.visualFocus ? 2 : 1
                                radius: 3
                        }
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
                height: col2.implicitHeight + 2 * contentPadding
                color: "white"
                Column{
                    id: col2
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: qsTr("Propre par défaut")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    ComboBox{
                        id: cB2
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        model: ["Roman","Australian","American","Brazilian","Canadian","English","French","New-Zealander","Polish","Portugese","Scottish","Spanish","Welsh"]
                        background: Rectangle {
                                implicitWidth: 120
                                implicitHeight: 40
                                border.color: cB2.focus ? "#55ACEE" : "grey"
                                border.width: cB2.visualFocus ? 2 : 1
                                radius: 3
                        }
                    }
                }
            }
        }
    }
}
