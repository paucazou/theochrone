/* Theme Name: Worthy - Free Powerful Theme by HtmlCoder
 * Author:HtmlCoder
 * Author URI:http://www.htmlcoder.me
 * Version:1.0.0
 * Created:November 2014
 * License: Creative Commons Attribution 3.0 License (https://creativecommons.org/licenses/by/3.0/)
 * File Description: Place here your custom scripts
 */


function makeHSubmenuVisible(elt) {
    var classname = elt.getAttribute('class').replace("hmenu ","");
    console.log(classname);
    var menu = document.getElementsByClassName("hsubmenu closed " + classname);
    console.log("menu : ");
    var length = menu.length;
    var new_classname = menu[0].getAttribute("class").replace("closed","opened");
    for (var i = 0; i < length; i++) {
        menu[0].setAttribute("class",new_classname);
        }
    //elt.setAttribute("onclick", "hideHSubmenu(this)");
    var caret = elt.getElementsByClassName("fa-caret-down")[0];
    //console.log(caret);
    caret.setAttribute("class","fa fa-caret-right");
}

$(document).click(function(event){
    var hsubmenu_opened = document.getElementsByClassName("hsubmenu opened");
    console.log("hsubmenu_opened : ");
    console.log(hsubmenu_opened);
    var length = hsubmenu_opened.length;
    for (var i = 0; i < length; i++) {
        var new_classname = hsubmenu_opened[0].getAttribute("class").replace("opened","closed");
       hsubmenu_opened[0].setAttribute("class",new_classname);
        }
    var caret = document.getElementsByClassName("fa-caret-right");
    //console.log(caret);
    for (var i = 0; i < caret.length; i++) {
        caret[i].setAttribute("class","fa fa-caret-down");
    }
    var eclassname = event.target.getAttribute("class");
    //console.log(eclassname);
    if ( eclassname.indexOf("hmenu") > -1) {
        makeHSubmenuVisible(event.target);
    }
}
            )
