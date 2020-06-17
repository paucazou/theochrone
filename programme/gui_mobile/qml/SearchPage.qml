import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12

Page {
    id: searchPage
    title: qsTr("Recherche")

    property int maxWidth: 500
    property int contentPadding: 20

    ScrollView{
        anchors.fill: parent
        ColumnLayout{
            anchors.fill: parent
            spacing: 0
            height: switchContainer.height + 5 + searchKeywordsCont.height + 5 + searchWeekCont.height + 5 + searchMonthCont.height + 5 + searchYearCont.height + 5 + searchTimeCont.height
            Rectangle{
                id: switchContainer
                Layout.fillWidth: true
                Layout.maximumWidth: maxWidth
                Layout.alignment: Qt.AlignCenter
                height: 140
                Column {
                    anchors.fill: parent
                    padding: contentPadding
                    Switch{
                        text: "Rechercher dans le martyrologue Romain"
                    }
                    Switch{
                        text: "Inclure les messes Pro Aliquibus Locis"
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
                height: 210
                color: "white"
                Column{
                    id: colKeywords
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Recherche par mots-clefs")
                        color: "#55ACEE"
                        font.pixelSize: 20
                    }
                    TextField{
                        placeholderText: qsTr("Entrez vos mots-clefs:")
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        topPadding: 10
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
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["2019","2020","2021"]
                        }
                        Button{
                            text: qsTr("OK")
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
                height: 170
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Rechercher une semaine toute entière")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["2019","2020","2021"]
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: [qsTr("Janvier"),qsTr("Février"),qsTr("Mars"),qsTr("Avril"),qsTr("Mai"),qsTr("Juin"),qsTr("Juillet"),qsTr("Août"),qsTr("Septembre"),qsTr("Octobre"),qsTr("Novembre"),qsTr("Décembre")]
                        }
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["Première semaine","Deuxième semaine","Troisième semaine","Quatrième semaine"]
                        }
                        Button{
                            text: qsTr("OK")
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
                height: 170
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Rechercher un mois tout entier")
                        color: "#55ACEE"
                        font.pixelSize: 20
                        bottomPadding: 10
                    }
                    RowLayout{
                        anchors{
                            left: parent.left
                            right: parent.right
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["2019","2020","2021"]
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: [qsTr("Janvier"),qsTr("Février"),qsTr("Mars"),qsTr("Avril"),qsTr("Mai"),qsTr("Juin"),qsTr("Juillet"),qsTr("Août"),qsTr("Septembre"),qsTr("Octobre"),qsTr("Novembre"),qsTr("Décembre")]
                        }
                    }
                    Button{
                        text: qsTr("OK")
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
                height: 170
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Rechercher une année toute entière")
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
                    Button{
                        text: qsTr("OK")
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
                height: 240
                color: "white"
                Column{
                    anchors.fill: parent
                    anchors.margins: contentPadding
                    Text {
                        text: qsTr("Rechercher une durée libre")
                        color: "#55ACEE"
                        font.pixelSize: 20
                    }
                    Text {
                        text: qsTr("Date de début")
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
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","29","30","31"]
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: [qsTr("Janvier"),qsTr("Février"),qsTr("Mars"),qsTr("Avril"),qsTr("Mai"),qsTr("Juin"),qsTr("Juillet"),qsTr("Août"),qsTr("Septembre"),qsTr("Octobre"),qsTr("Novembre"),qsTr("Décembre")]
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["2019","2020","2021"]
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
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","29","30","31"]
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: [qsTr("Janvier"),qsTr("Février"),qsTr("Mars"),qsTr("Avril"),qsTr("Mai"),qsTr("Juin"),qsTr("Juillet"),qsTr("Août"),qsTr("Septembre"),qsTr("Octobre"),qsTr("Novembre"),qsTr("Décembre")]
                        }
                        ComboBox{
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: ["2019","2020","2021"]
                        }
                    }
                }
            }
        }
    }
}
