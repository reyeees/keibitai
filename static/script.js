

class Images {
    constructor(index, percents, hash_f, hash_s, url_f, url_s) {
        this.index = index;
        this.percents = percents;
        this.hash_f = hash_f;
        this.hash_s = hash_s;
        this.url_f = url_f;
        this.url_s = url_s;
    }

    appear() {
        var first = home_url("/file?f=".concat(encodeURIComponent(this.url_f)));
        var second = home_url("/file?f=".concat(encodeURIComponent(this.url_s)));

        const div = document.createElement("div");
        div.classList.add("images");
        div.innerHTML = `
            <div id="imager">
                <div id="images" onclick=fdelete("${this.url_f}")>
                    <img id="image" src="${first}" alt="First image" />
                    <p><span>${this.hash_f}</span></p>
                </div>
                <div id="percents">
                    <p onclick=save(${this.index})><span>${this.percents}%</span></p>
                </div>
                <div id="images" onclick=fdelete("${this.url_s}")>
                    <img id="image" src="${second}" alt="Second image" />
                    <p><span>${this.hash_s}</span></p>
                </div>
            </div>
        `;

        return div;
    }
}

var index = 0;
var images = [];

// function httpGetAsync(theUrl, callback) {
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.onreadystatechange = function() {
//         if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
//         callback(xmlHttp.responseText);
//     }
//     xmlHttp.open("GET", theUrl, true);
//     xmlHttp.send(null);
// };

function fdelete(pfilename) {
    var response = httpGet("/delete?f=".concat(encodeURIComponent(pfilename)));
    console.log(response);
}

function save(pindex) {
    var response = httpGet("/save?index=".concat(pindex.toString()));
    console.log(response);
}

document.addEventListener("DOMContentLoaded", function() {
    const feed = document.getElementById("feed");

    while (true) {
        var response = httpGet("/index?index=".concat(index.toString()));
        console.log(response);
        if (response["message"] != "SUCCESS") { // Invalid request: Index out of bounds.
            break;
        } else {
            images.push(new Images(
                index,
                response["percents"],
                response["first_hash"],
                response["second_hash"],
                response["first_filename"],
                response["second_filename"]
            ));
            index += 1;
        }
    }
    
    for (var i = 0; i < images.length; i++) {
        feed.appendChild(images[i].appear());
    }
});


// document.onkeydown = function (e) {
//     // console.log(e.keyCode); // 13
//     if (e.keyCode == 37 || e.keyCode == 81) { // back function. arrow-left or Q
//         ok_button.click();
//     }
//     if (e.keyCode == 39 || e.keyCode == 69) { // next function. arrow-right or E
//         next_button.click();
//     }
//     if (e.keyCode == 13) {
//         save();
//     } // Return or Enter
// };
