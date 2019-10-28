import QtQuick 2.12

Item {
    id: app
    anchors.fill: parent
    opacity: 0.0

    Behavior on opacity { NumberAnimation { duration: 500 } }

    function init()
    {
        opacity = 1.0

    }

}
