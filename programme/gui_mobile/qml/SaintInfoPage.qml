import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12

Page {
    id: saintInfoPage
    title: qsTr("Résultat")

    // MAJ data
    Connections {
        target: feast
        function onChangeSignal() {
            model.clear()
            for(var i = 0; i < feast.getNbElements(); i++){
                model.append(feast.getData(i))
            }
        }
    }


    property int maxWidth: 500
    property int contentPadding: 20

    property int myFirstCurrentIndex: 0
    onMyFirstCurrentIndexChanged: {
        swipeView.currentIndex = myFirstCurrentIndex;
    }

    SwipeView{
        id: swipeView
        anchors.fill: parent

        // Manage changement on title
        // model must be fully loaded in the beginnig, then
        onCurrentIndexChanged: {
            if (modelFullLoaded == true)
            {
                saintInfoPage.title = swipeView.currentItem.item.nF
            }
        }
        property bool modelFullLoaded: false
        onModelFullLoadedChanged: {
            saintInfoPage.title = swipeView.currentItem.item.nF // (first) change the title of the page
        }

        Repeater{
            id: repeater
            model: ListModel{
                id: model
                Component.onCompleted: {
                    for(var i = 0; i < feast.getNbElements(); i++){
                        model.append(feast.getData(i))
                    }
                    swipeView.modelFullLoaded = true
                }
            }
            Loader{
                active: SwipeView.isCurrentItem || SwipeView.isNextItem || SwipeView.isPreviousItem
                sourceComponent: activeFrame
                Component{
                    id: activeFrame
                    ScrollView{
                        property var nF: nameFest    // For change the title of the page
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
                                        height: mT.implicitHeight
                                        color: "#F5F5F5"
                                        Text {
                                            id: mT
                                            text: qsTr("Textes de la messe et de l'office sur Intoibo.fr")
                                            color: "#55ACEE"
                                            padding: 15
                                            clip: true
                                            width: parent.width
                                            wrapMode: Text.Wrap
                                        }
                                        MouseArea{
                                            anchors.fill: parent
                                            onClicked: Qt.openUrlExternally(massText);
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
    Rectangle{
        height: indicator.height
        width: indicator.width
        color: "lightgrey"
        radius: height / 2
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        anchors.horizontalCenter: parent.horizontalCenter
        visible: repeater.count > 1 && width < (parent.width - 5) ? true : false    // useful for the research
        PageIndicator{
            id: indicator
            currentIndex: swipeView.currentIndex
            count: repeater.count
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
