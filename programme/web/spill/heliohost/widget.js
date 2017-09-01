var iwtheo; // iframe content window
var ifratheo = document.getElementById("theowidget");
ifratheo.src = "https://theochrone.ga/static/shtml/main.shtml" // to correct slowness of HelioHost
var bsurl = "https://theochrone.ga";
var surl = bsurl + "/static/shtml/main.shtml";
console.log(surl);

// send message to server
ifratheo.onload = function (){
    console.log('loaded');
    var iwtheo = ifratheo.contentWindow;
    iwtheo.postMessage("God sees you",surl);
    console.log('Message sent');
};
// listener
window.addEventListener("message", function(event){
    if (event.origin == bsurl){
        if (event.data == "set container to 0px"){
            document.getElementById("theocontainer").style.height = "0px";
        } else {
    document.getElementById("theocontainer").style.height = event.data+'px';
        }
    }
}, false);
