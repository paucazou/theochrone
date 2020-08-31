import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12
import QtQml 2.14

Page {
    id: searchPage
    title: qsTr("Recherche")

    property int maxWidth: 500
    property int contentPadding: 20
    property date currentTime: new Date()

    ScrollView{
        anchors.fill: parent
        ColumnLayout{
            anchors.fill: parent
            spacing: 0
            Rectangle{
                id: switchContainer
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: col1.implicitHeight + 2 * contentPadding
                Column {
                    id: col1
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Switch{
                        id: s1
                        text: qsTr("Rechercher dans le martyrologue Romain")
                        width: parent.width
                        clip: true
                        contentItem: Text {
                            text: s1.text
                            font: s1.font
                            wrapMode: Text.WordWrap
                            color: s1.checked ? "black" : "grey"
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: s1.indicator.width + s1.spacing
                        }
                    }
                    Switch{
                        id: s2
                        text: qsTr("Inclure les messes Pro Aliquibus Locis")
                        width: parent.width
                        clip: true
                        contentItem: Text {
                            text: s2.text
                            font: s2.font
                            wrapMode: Text.WordWrap
                            color: s2.checked ? "black" : "grey"
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: s2.indicator.width + s2.spacing
                        }
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        Text {
                            text: qsTr("Prope")
                            Layout.alignment: Qt.AlignVCenter
                        }
                        ComboBox{
                            id: cB1
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: listLang
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
                id: searchKeywordsCont
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
                        text: qsTr("Recherche par mots-clefs")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    TextField{
                        id: searchTexField
                        placeholderText: qsTr("Entrez vos mots-clefs:")
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        topPadding: 15
                        leftPadding: 10
                        rightPadding: 10
                        background: Rectangle {
                                implicitWidth: searchTexField.width
                                implicitHeight: searchTexField.height
                                border.color: searchTexField.focus ? "#55ACEE" : "grey"
                                border.width: 0.5
                                radius: 3
                            }
                    }
                    Switch{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        text: qsTr("Plus de résultats")
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            id: cB2
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: comboYears
                            Component.onCompleted: {

                                currentIndex=cB2.find(currentTime.getFullYear());
                            }
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB2.focus ? "#55ACEE" : "grey"
                                    border.width: cB2.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        Button{
                            text: qsTr("Chercher")
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                        }
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
                id: searchWeekCont
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: col3.implicitHeight + 2 * contentPadding
                color: "white"
                Column{
                    id: col3
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: qsTr("Rechercher une semaine")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            id: cB3
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: comboYears
                            Component.onCompleted: {

                                currentIndex=cB3.find(currentTime.getFullYear());
                            }
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB3.focus ? "#55ACEE" : "grey"
                                    border.width: cB3.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        ComboBox{
                            id: cB4
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: listMonth
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB4.focus ? "#55ACEE" : "grey"
                                    border.width: cB4.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            id: cB5
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: [qsTr("Première semaine"),qsTr("Deuxième semaine"),qsTr("Troisième semaine"),qsTr("Quatrième semaine")]
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB5.focus ? "#55ACEE" : "grey"
                                    border.width: cB5.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        Button{
                            text: qsTr("Chercher")
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                        }
                    }
                }
            }
            Rectangle{
                id: thirdSeparateLine
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
                id: searchMonthCont
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: col4.implicitHeight + 2 * contentPadding
                color: "white"
                Column{
                    id: col4
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: qsTr("Rechercher un mois")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            id: cB6
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: comboYears
                            Component.onCompleted: {

                                currentIndex=cB6.find(currentTime.getFullYear());
                            }
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB6.focus ? "#55ACEE" : "grey"
                                    border.width: cB6.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        ComboBox{
                            id: cB7
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: listMonth
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB7.focus ? "#55ACEE" : "grey"
                                    border.width: cB7.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                    }
                    Button{
                        text: qsTr("Chercher")
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                    }
                }
            }
            Rectangle{
                id: fourthSeparateLine
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
                id: searchYearCont
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: col5.implicitHeight + 2 * contentPadding
                color: "white"
                Column{
                    id: col5
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: qsTr("Rechercher une année")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    ComboBox{
                        id: cB8
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        model: comboYears
                        Component.onCompleted: {

                            currentIndex=cB8.find(currentTime.getFullYear());
                        }
                        background: Rectangle {
                                implicitWidth: 120
                                implicitHeight: 40
                                border.color: cB8.focus ? "#55ACEE" : "grey"
                                border.width: cB8.visualFocus ? 2 : 1
                                radius: 3
                        }
                    }
                    Button{
                        text: qsTr("Chercher")
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                    }
                }
            }
            Rectangle{
                id: fithSeparateLine
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
                id: searchTimeCont
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: col6.implicitHeight + 2 * contentPadding
                color: "white"
                Column{
                    id: col6
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: contentPadding
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        text: qsTr("Rechercher une durée libre")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                        wrapMode: Text.WordWrap
                        width: parent.width
                        clip: true
                    }
                    Text {
                        text: qsTr("Date de début")
                        color: "#181818"
                        font.pixelSize: 15
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            id: cB9
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","29","30","31"]
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB9.focus ? "#55ACEE" : "grey"
                                    border.width: cB9.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        ComboBox{
                            id: cB10
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: listMonth
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB10.focus ? "#55ACEE" : "grey"
                                    border.width: cB10.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        ComboBox{
                            id: cB11
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: comboYears
                            Component.onCompleted: {

                                currentIndex=cB11.find(currentTime.getFullYear());
                            }
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB11.focus ? "#55ACEE" : "grey"
                                    border.width: cB11.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                    }
                    Text {
                        text: qsTr("Date de fin")
                        color: "#181818"
                        font.pixelSize: 15
                        topPadding: 10
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            id: cB12
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","29","30","31"]
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB12.focus ? "#55ACEE" : "grey"
                                    border.width: cB12.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        ComboBox{
                            id: cB13
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: listMonth
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB13.focus ? "#55ACEE" : "grey"
                                    border.width: cB13.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                        ComboBox{
                            id: cB14
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: comboYears
                            Component.onCompleted: {

                                currentIndex=cB14.find(currentTime.getFullYear());
                            }
                            background: Rectangle {
                                    implicitWidth: 120
                                    implicitHeight: 40
                                    border.color: cB14.focus ? "#55ACEE" : "grey"
                                    border.width: cB14.visualFocus ? 2 : 1
                                    radius: 3
                            }
                        }
                    }
                }
            }
        }
    }
}
