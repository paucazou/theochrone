import QtQuick 2.12

Rectangle    {
    id: titleBar
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.right: parent.right
    height: GameSettings.fieldHeight //60 //GameSettings.fieldHeight #########################!!! ATTENTION REMETTRE APRES
    color: GameSettings.viewColor


    signal titleClicked(int index)

    Rectangle{
        id: borderGradient
        width: parent.width
        height: 7
        gradient: Gradient {
                GradientStop { position: 0.3; color: "#00ffffff" }
                GradientStop { position: 2.0; color: "grey" }
        }
    }

}
