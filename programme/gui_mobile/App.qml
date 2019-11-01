import QtQuick 2.12

Item {
    id: app
    anchors.fill: parent
    opacity: 0.0

    //Animation sur l'opacité
    Behavior on opacity { NumberAnimation { duration: 500 } }

    property var pages: ["pages/Home.qml",
                         "pages/Calendar.qml",
                         "pages/Resources.qml",
                         "pages/Settings.qml"]

    property int __currentIndex: 0

    function init()
    {
        opacity = 1.0
        __currentIndex = 0
        pageLoader.setSource(pages[0])
    }
    function nextPage()
    {
        pageLoader.setSource(pages[__currentIndex]);
    }

    Loader {
        id: pageLoader
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: headerBar.bottom
        anchors.bottom: parent.bottom

        onStatusChanged: {
            if (status === Loader.Ready)
            {
                pageLoader.item.init();
                pageLoader.item.forceActiveFocus()
            }
        }
    }

    HeaderBar{
        id: headerBar
    }

    TitleBar {
        id: titleBar
        currentIndex: __currentIndex

        onTitleClicked: {
            if (index != __currentIndex)
                __currentIndex = index
                pageLoader.item.close()
        }
    }

    Keys.onReleased: {  //user interaction to quit
        switch (event.key) {
        case Qt.Key_Escape:
        case Qt.Key_Back: {
            if (__currentIndex > 0) {
                pageLoader.item.close()
                event.accepted = true
            } else {
                Qt.quit()
            }
            break;
        }
        default: break;
        }
    }

}
