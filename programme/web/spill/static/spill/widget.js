var iwtheo; // iframe content window
var ifratheo = document.getElementById("theowidget");
var theocontainer = document.getElementById("theocontainer");
console.log(ifratheo.src);
var bsurl = ifratheo.src.split('/spill',1)[0]; // get the url requested by user. It will match with the url of the content, which can be either url possible, even other created by other users
var surl = bsurl + "/spill/main";
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
    document.getElementById("theocontainer").style.height = event.data+'px'; // add one or two pixels
        }
    }
}, false);
