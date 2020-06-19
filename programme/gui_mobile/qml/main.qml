import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Material 2.12
import QtGraphicalEffects 1.14


ApplicationWindow {
    id: window
    visible: true
    width: 640
    height: 480
    title: qsTr("Theochrone")
    color: "#55ACEE"

    header: ToolBar {
        contentHeight: toolButton.implicitHeight

        ToolButton {
            id: toolButton
            Image {
                source: stackView.depth > 1 ? "qrc:/images/icons/round_arrow_back_white_48.png"
                                            : "qrc:/images/icons/round_menu_white_48.png"
                anchors.centerIn: parent
                width: parent.height * 0.5
                height: parent.width * 0.5
            }
            font.pixelSize: Qt.application.font.pixelSize * 1.6
            onClicked: {
                if (stackView.depth > 1)
                {
                    stackView.pop();
                }
                else
                {
                    drawer.open();
                }
            }
        }

        Label {
            text: stackView.currentItem.title
            font.pixelSize: 20
            color: "white"
            anchors.centerIn: parent
        }

        ToolButton {
            id: layoutButton
            anchors.right: parent.right
            anchors.rightMargin: 5
            visible:  stackView.depth > 1 ? false : true
            Image {
                source: "qrc:/images/icons/round_view_list_white_48.png"
                anchors.centerIn: parent
                width: parent.height * 0.5
                height: parent.width * 0.5
            }
            onClicked: {
                stackView.currentItem.myCarouselFestView = !stackView.currentItem.myCarouselFestView;
            }
        }
        ToolButton {
            id: searchButton
            anchors.right: layoutButton.left
            anchors.rightMargin: 5
            visible:  stackView.depth > 1 ? false : true
            Image {
                source: "qrc:/images/icons/round_search_white_48.png"
                anchors.centerIn: parent
                width: parent.height * 0.5
                height: parent.width * 0.5
            }
            onClicked: {
                stackView.push("qrc:/qml/SearchPage.qml")
            }
        }
    }

    Drawer {
        id: drawer
        width: 400 * 0.80
        height: window.height


        Item{
            id: encapsuleDrawer //anchors don't work directly on Drawer
            anchors.fill: parent

            Rectangle{
                id: drawerLogo
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                width: parent.width
                height: width * 0.693
                color: "#FFFFFF"
                Image {
                    id: name
                    source: "qrc:/images/background/background.jpg"
                    anchors.fill: parent
                }
                Image{
                    id: drawerLogoImg
                    source: "qrc:/images/logo/logo.png"
                    width: drawerLogo.width * 0.3
                    height: width * 1.056
                    anchors.centerIn: parent
                }
                Glow{
                    anchors.fill: drawerLogoImg
                    radius: 5
                    color: "white"
                    source: drawerLogoImg
                }
            }

            Rectangle{
                id: separator
                anchors.top: drawerLogo.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: 40
                color: "#55ACEE"
                Text {
                    id: version
                    text: qsTr("Ad majorem Dei gloriam")
                    anchors.centerIn: parent
                    color: "white"
                }
            }

            ScrollView{
                anchors.top: separator.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                clip: true

                Column {
                    anchors.fill: parent

                    ItemDelegate {
                        text: qsTr("Paramètres")
                        width: parent.width
                        icon.source: "qrc:/images/icons/outline_settings_black_48.png"
                        icon.color: "#55ACEE"
                        onClicked: {
                            stackView.push("qrc:/qml/SettingsPage.qml")
                            drawer.close()
                        }
                    }
                    Rectangle{
                        anchors.left: parent.left
                        anchors.right: parent.right
                        height: 1
                        color: "#DCDCDC"
                    }
                    ItemDelegate {
                        text: qsTr("Exporter en PDF")
                        width: parent.width
                        icon.source: "qrc:/images/icons/icons8-pdf-100.png"
                        icon.color: "#55ACEE"
                        onClicked: {
                        }
                    }
                    ItemDelegate {
                        text: qsTr("Exporter vers votre calendrier")
                        width: parent.width
                        icon.source: "qrc:/images/icons/icons8-ICS-100.png"
                        icon.color: "#55ACEE"
                        onClicked: {
                        }
                    }
                    Rectangle{
                        anchors.left: parent.left
                        anchors.right: parent.right
                        height: 1
                        color: "#DCDCDC"
                    }
                    ItemDelegate {
                        text: qsTr("Site web")
                        width: parent.width
                        icon.source: "qrc:/images/icons/outline_public_black_48.png"
                        icon.color: "#55ACEE"
                        onClicked: {
                            Qt.openUrlExternally("https://theochrone.fr");
                        }
                    }
                    ItemDelegate {
                        text: qsTr("Quitter")
                        width: parent.width
                        icon.source: "qrc:/images/icons/round_exit_to_app_black_48.png"
                        icon.color: "#55ACEE"
                        onClicked: {
                            Qt.quit();
                        }
                    }
                }
            }
        }
    }

    StackView {
        id: stackView
        initialItem: "qrc:/qml/HomePage.qml"
        anchors.fill: parent
    }

    onClosing: {
            if(stackView.depth > 1)
            {
                close.accepted = false;
                stackView.pop();
            }
            else
            {
                close.accepted = true;
            }
        }
}
