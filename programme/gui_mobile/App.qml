import QtQuick 2.12

Item {
    id: app
    anchors.fill: parent
    opacity: 0.0

    Behavior on opacity { NumberAnimation { duration: 500 } }

    property var lastPages: []
    property int __currentIndex: 0

    function init()
    {
        opacity = 1.0
        showPage("Home.qml")
    }
    function prevPage()
    {
        lastPages.pop()
        pageLoader.setSource(lastPages[lastPages.length-1])
        __currentIndex = lastPages.length-1;
    }
    function showPage(name)
    {
        lastPages.push(name)
        pageLoader.setSource(name)
        __currentIndex = lastPages.length-1;
    }

    TitleBar {
        id: titleBar
        currentIndex: __currentIndex

        onTitleClicked: {
            if (index < __currentIndex)
                pageLoader.item.close()
        }
    }

    Loader {
        id: pageLoader
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: titleBar.top

        onStatusChanged: {
            if (status === Loader.Ready)    //loading next page
            {
                //pageLoader.item.init();
                pageLoader.item.forceActiveFocus()
            }
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
