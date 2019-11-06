import QtQuick 2.12
import QtQuick.Controls 2.12

GamePage {
    property int nbFest: 2 /* A CHANGER */

    ListModel {
        id: contactModelTitleFest

        ListElement {
            fest: "Fest of the day 2"
        }

        ListElement {
            fest: "Fest of the day 1"
        }
    }

    Component {
        id: contactTitleFest
        Item {
            id: festContainer
            width: parent.width
            height: 2*40 /* CHANGER par heightField gammesettings */

            signal titleClicked()
            onTitleClicked: {
                console.log("Click OK")
            }

            Item {
                id: titleFest
                anchors.centerIn: parent
                width: parent.width - 20
                height: parent.height - 20

                Rectangle{
                    id: backgroundTitleFest
                    width: parent.width
                    height: parent.height
                    color: "#55ACEE"
                    radius: 10

                    Text {
                        anchors.centerIn: parent
                        text: fest
                    }
                }

                MouseArea{
                    anchors.fill: parent
                    onClicked: titleClicked()
                }
            }
        }
    }

    Rectangle{
        anchors.fill: parent

        ListView{
            anchors.fill: parent
            model: contactModelTitleFest
            delegate: contactTitleFest
            focus: true
        }
    }
}
