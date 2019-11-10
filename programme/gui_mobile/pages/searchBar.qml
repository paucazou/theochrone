import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

ToolBar {

    property bool busyIndicatorRunning : false
    property bool searchBarVisbile: true

    signal doSearch(string searchText)
    signal searchTextChanged(string searchText)
    signal showCategories()
    signal goBack()
    signal showMap()

    onSearchBarVisbileChanged: {
        searchBar.opacity = searchBarVisbile ? 1 : 0
        backBar.opacity = searchBarVisbile ? 0 : 1
    }

    function showSearch(text) {
        if (text != null) {
            searchText.ignoreTextChange = true
            searchText.text = text
            searchText.ignoreTextChange = false
        }
    }

    RowLayout {
        id: searchBar
        width: parent.width
        height: parent.height
        Behavior on opacity { NumberAnimation{} }
        visible: opacity ? true : false
        TextField {
            id: searchText
            Behavior on opacity { NumberAnimation{} }
            visible: opacity ? true : false
            property bool ignoreTextChange: false
            placeholderText: qsTr("Search")
            Layout.fillWidth: true
            onTextChanged: {
                if (!ignoreTextChange)
                    searchTextChanged(text)
            }
            onAccepted: doSearch(searchText.text)
        }
        ToolButton {
            id: searchButton
            iconSource:  "../../resources/search.png"
            onClicked: doSearch(searchText.text)
        }
        ToolButton {
            id: categoryButton
            iconSource:  "../../resources/categories.png"
            onClicked: showCategories()
        }
    }

    RowLayout {
        id: backBar
        width: parent.width
        height: parent.height
        opacity: 0
        Behavior on opacity { NumberAnimation{} }
        visible: opacity ? true : false
        ToolButton {
            id: backButton
            iconSource:  "../../resources/left.png"
            onClicked: goBack()
        }
        ToolButton {
            id: mapButton
            iconSource:  "../../resources/search.png"
            onClicked: showMap()
        }
        Item {
             Layout.fillWidth: true
        }
    }
}