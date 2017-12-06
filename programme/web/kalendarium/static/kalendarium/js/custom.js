/* Theme Name: Worthy - Free Powerful Theme by HtmlCoder
 * Author:HtmlCoder
 * Author URI:http://www.htmlcoder.me
 * Version:1.0.0
 * Created:November 2014
 * License: Creative Commons Attribution 3.0 License (https://creativecommons.org/licenses/by/3.0/)
 * File Description: Place here your custom scripts
 */


/*function makeHSubmenuVisible(elt) {
    var classname = elt.getAttribute('class').replace("hmenu ","");
    elt.setAttribute('class',elt.getAttribute('class') + " opened");
    //console.log(classname);
    var menu = document.getElementsByClassName("hsubmenu closed " + classname);
    //console.log("menu : ");
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
     var hmenu_opened = document.getElementsByClassName('hmenu');
     console.log(hmenu_opened);
    //console.log("hsubmenu_opened : ");
    //console.log(hsubmenu_opened);
     var length = hsubmenu_opened.length;
     for (var i = 0; i < length; i++) {        
        var new_classname = hsubmenu_opened[0].getAttribute("class").replace("opened","closed");
       hsubmenu_opened[0].setAttribute("class",new_classname);
         }
    var caret = document.getElementById('navbar-collapse-1').getElementsByClassName("fa-caret-right");
    //console.log(caret);
    for (var i = 0; i < caret.length; i++) {
        caret[i].setAttribute("class","fa fa-caret-down");
    }
    var eclassname = event.target.getAttribute("class");
    //console.log(eclassname);
    if ( eclassname.indexOf("hmenu") > -1) {
        event.preventDefault();
        var elt = event.target;
//         console.log(eclassname);
        if ( eclassname.indexOf("opened") > - 1) {
            //elt.setAttribute('class',elt.getAttribute('class').replace("opened","closed"));
        }
        else {            
        makeHSubmenuVisible(event.target);
        }
    }
}
            )*/


function toggleHmenu(elt,disable_it){ // elt is hmenu, disable_it is a boolean
    // disable or not elt
    elt.setAttribute('disabled',disable_it);
    // disable or not childre
    var children = $("a[menu-parent='" + elt.getAttribute("children") + "']");
    for (var i=0;i < children.length; i++){
        children[i].setAttribute('disabled',disable_it);
    }
    // changing caret
    var caret = elt.getElementsByTagName('i')[0];
    if (disable_it){
        caret.setAttribute('class',"fa fa-caret-down");
    }
    else {
        caret.setAttribute('class',"fa fa-caret-right");
    }
    
}

$(document).click(function(event){
    var target = event.target;
    var hmenus = document.getElementsByClassName('hmenu');
    var default_menu_name = '';
//     console.log(target);
    if (target.getAttribute('class') == 'hmenu'){ // click on hmenu
        event.preventDefault();
        // displaying or disabling target and children of target if necessary
        var disable_it = !Boolean(target.getAttribute('disabled') == 'true');
        toggleHmenu(target,disable_it);
        //console.log(disable_it);
        default_menu_name = target.getAttribute('children');
        }
    // disabling all hmenus
    for (var i=0; i < hmenus.length; i++) {
        if (hmenus[i].getAttribute('children') != default_menu_name){
            toggleHmenu(hmenus[i],true);
        }
    }
}    
)
