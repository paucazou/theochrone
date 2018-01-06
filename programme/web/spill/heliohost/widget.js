var iwtheo; // iframe content window
var ifratheo = document.getElementById("theowidget");
// switch to static
var static_url = "https://theochrone.ga/static/shtml/main.shtml"
var params = ifratheo.src.split('?');
//ifratheo.src = static_url;
console.log(ifratheo.src);
var suffix = ifratheo.src.split('.')[1].split('/')[0];
var bsurl = "https://theochrone."+suffix;
var surl = bsurl + "/static/shtml/main.shtml?" + params[1];
console.log(surl);
ifratheo.src = surl;

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
