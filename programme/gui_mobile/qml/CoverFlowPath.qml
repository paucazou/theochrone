import QtQuick 2.0

// 5 points
//    PathLine | PathQuad  | PathLine
// * ---------- *                 * ---------- *
//                   ----- * -----

Path {
    // Point 1
    property PathView pathView

    // This determines where the left edge of the path starts
    startX: 0
    startY: pathView.vertOff

    PathAttribute {
        name: "rotateY"
        value: 60.0
    }
    PathAttribute {
        name: "scale"
        value: 0.7
    }
    PathAttribute {
        name: "zOrder"
        value: 10.0
    }

    // Line to point 2
    PathLine {
        x: pathView.centerX - pathView.picSize * 0.4
        y: pathView.vertOff
    }
    PathPercent {
        value: 0.30
    }
    PathAttribute {
        name: "rotateY"
        value: 60.0
    }
    PathAttribute {
        name: "scale"
        value: 0.7
    }
    PathAttribute {
        name: "zOrder"
        value: 10.0
    }

    // Quad to point 3
    PathQuad {
        x: pathView.centerX
        y: pathView.vertOff + pathView.picSize * 0.04
        controlX: pathView.centerX - pathView.picSize * 0.2
        controlY: pathView.vertOff + pathView.picSize * 0.04
    }
    PathPercent {
        value: 0.5
    }
    PathAttribute {
        name: "rotateY"
        value: 0.0
    }
    PathAttribute {
        name: "scale"
        value: 1.0
    }
    PathAttribute {
        name: "zOrder"
        value: 50.0
    }

    // Quad to point 4
    PathQuad {
        x: pathView.centerX + pathView.picSize * 0.4
        y: pathView.vertOff
        controlX: pathView.centerX + pathView.picSize * 0.2
        controlY: pathView.vertOff + pathView.picSize * 0.04
    }
    PathPercent {
        value: 0.70
    }
    PathAttribute {
        name: "rotateY"
        value: -60.0
    }
    PathAttribute {
        name: "scale"
        value: 0.7
    }
    PathAttribute {
        name: "zOrder"
        value: 10.0
    }

    // Line to point 5
    PathLine {
        // This determines where the right edge of the path starts
        x: pathView.width
        y: pathView.vertOff
    }
    PathAttribute {
        name: "rotateY"
        value: -60.0
    }
    PathAttribute {
        name: "scale"
        value: 0.7
    }
    PathAttribute {
        name: "zOrder"
        value: 10.0
    }
}
