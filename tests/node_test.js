//This file contains tests called with node
//

const fs= require('fs');
const resolve = require('path').resolve;
const zombie = require('../node_modules/zombie');

function test_todivinumofficium() {
	// load data
	var today = new Date();
	var path = resolve("../programme/web/kalendarium/static/kalendarium/todivinumofficium.html"); // this path may be broken.
	var get_values = "?day=" + today.getDate() + "&month=" + (today.getMonth() + 1) + "&year=" + today.getFullYear() + "&lang=fr&office=mass"; // lang and office for now
	var link = "file://" + path + get_values;
	//var content = fs.readFileSync(path).toString();

	// setting browser
	/*new zombie({debug: true}).visit("file://"+link,
		function (error,browser) {
			console.log(error);
		});*/
	const browser = new zombie();
	var page = browser.visit(link,function() {
//		console.log(browser.html("form"));
		console.log(browser.error);
//		console.log(browser.html("script"));
		//browser.assert.url("http://divinumofficium.com/cgi-bin/missa/missa.pl");
		/*browser.clickLink(".ifneeded",function(error,browser,status){
		console.log(error);
		});*/
	}
	);




}

test_todivinumofficium();
