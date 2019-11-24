pragma Singleton
import QtQuick 2.5

Item {
    property int wHeight
    property int wWidth

    // Colors
        //color blue theme tehochrone: #55ACEE
    readonly property color backgroundColor: "#55ACEE"
    readonly property color buttonColor: "#ffffff"
    readonly property color buttonPressedColor: "#6ccaf2"
    readonly property color disabledButtonColor: "#555555"
    readonly property color viewColor: "#00ffffff"  //Transparent
    readonly property color delegate1Color: Qt.darker(viewColor, 1.2)
    readonly property color delegate2Color: Qt.lighter(viewColor, 1.2)
    readonly property color textColor: "#55ACEE"
    readonly property color textDarkColor: "#232323"
    readonly property color disabledTextColor: "#777777"
    readonly property color sliderColor: "#6ccaf2"
    readonly property color errorColor: "#ba3f62"
    readonly property color infoColor: "#3fba62"

    readonly property color liturgical_red: "#e02817"
    readonly property color liturgical_gold: "#FFD700"
    readonly property color liturgical_pink: "#ff7fdf"
    readonly property color liturgical_purple: "#7f3f7f"
    readonly property color liturgical_black: "#333333"
    readonly property color liturgical_white: "#e0e2e3"
    readonly property color liturgical_green: "#3ba338"

    // Font sizes
    property real microFontSize: hugeFontSize * 0.2
    property real tinyFontSize: hugeFontSize * 0.4
    property real smallTinyFontSize: hugeFontSize * 0.5
    property real smallFontSize: hugeFontSize * 0.6
    property real mediumFontSize: hugeFontSize * 0.7
    property real bigFontSize: hugeFontSize * 0.8
    property real largeFontSize: hugeFontSize * 0.9
    property real hugeFontSize: (wWidth + wHeight) * 0.03
    property real giganticFontSize: (wWidth + wHeight) * 0.04

    // Some other values
    property real fieldHeight: wHeight > wWidth ? wHeight * 0.08 : wWidth * 0.08
    property real fieldMargin: fieldHeight * 0.5
    property real buttonHeight: wHeight * 0.08
    property real buttonRadius: buttonHeight * 0.1

    // Some help functions
    function widthForHeight(h, ss)
    {
        return h/ss.height * ss.width;
    }

    function heightForWidth(w, ss)
    {
        return w/ss.width * ss.height;
    }

}
