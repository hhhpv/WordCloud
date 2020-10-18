// Core Logic Inspired By: https://codepen.io/stevn/pen/JdwNgw

// Main javascript File



// Modal Logic
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

function displaydiv() {
    console.log("her");
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

$('#word-cloud').on('click', 'div.mytooltip', function () {
    var show = document.getElementById("showing");
    show.innerHTML = "Now Showing Titles Related To Word: " + $(this).attr('title').toUpperCase();
    modal.style.display = "block";
    var w = $(this).attr('title').split(" ")[0];
    let m_arr = wordlistt["data"]["movie_list"][w];
    m_arr = new Set(m_arr)
    let mhtml = "<ol>";
    if (m_arr.length != 0) {
        m_arr.forEach(element => {
            mhtml += '<li><div class=\"w3-card\"><div class=\"row\"><div class=\"column\" style=\"text-align: center;\"><strong>&nbsp;&nbsp;' + element[0] + '</strong></div><div class=\"column\" style=\"text-align: center;\"><span style=\"font-style: italic;\">' + element[2] + '</span></div><div class=\"column\" style=\"text-align: center;\"><a href=\'' + element[1] + '\' target="_blank">Wiki <i class=\"fa fa-external-link\" aria-hidden=\"true\"></i></a></div></div></div></li>';
        });
    }
    mhtml += "</ol>";
    document.getElementById("movieList").innerHTML = mhtml;
});





//Global Variables
var wordsDown = [];
var wordlistt;
var freqListt;
var startPoint;
var cloud, traceCanvas;
var config;
var type = "top_words";
var genreMap = new Map();


// Genre Drop Down
genreMap.set("Sci-Fi", "sci");
genreMap.set("Action", "act");
genreMap.set("Drama", "dra");
genreMap.set("Comedy", "com");
genreMap.set("Biography", "bio");
genreMap.set("Adventure", "adv");
genreMap.set("Romance", "rom");
genreMap.set("Musical", "music");
var font;

$('#fontSelect a').on('click', function () {
    var txt = ($(this).text());
    $('#dropdownFontLink').html($(this).html());
    font = txt;
});
var year = "1900-1910";
$('#yearSelect a').on('click', function () {
    var txt = ($(this).text());
    $('#dropdownYearLink').html($(this).html());
    year = txt;
});
var genre = "com";
$('#genreSelect a').on('click', function () {
    var txt = ($(this).text());
    $('#dropdownGenreLink').html($(this).html());
    genre = genreMap.get(txt);
});
var noOfWords = "45"
var slider = document.getElementById("slider");
var output = document.getElementById("output");



// Dilip
// Set up an event handler for when the slider is changed
// To accomodate all browsers (IE), two events need to be set up.
slider.addEventListener("input", fixSlider);
slider.addEventListener("change", fixSlider);

function fixSlider(evt) {
    // If the value goes below 50, reset it to 50
    if (parseInt(this.value, 10) < 45) {
        this.value = 45;
    }
    output.textContent = this.value;
    noOfWords = this.value;
}






// Intial Set-Up:
function initialSetup(callback) {
    config = {
        trace: true,
        spiralResolution: 1,
        spiralLimit: 360 * 1000,
        lineHeight: 0.8,
        xWordPadding: 0,
        yWordPadding: 1,
        font: font,
    }

    cloud = document.getElementById("word-cloud");
    cloud.style.position = "relative";
    cloud.style.fontFamily = config.font;

    var traceCanvas = document.createElement("canvas");
    traceCanvas.style.borderColor = "black";
    traceCanvas.style.borderWidth = "thick";
    traceCanvas.setAttribute("id", "canvas");
    traceCanvas.width = window.innerWidth;
    traceCanvas.height = window.innerHeight;
    var traceCanvasCtx = traceCanvas.getContext("2d");
    cloud.appendChild(traceCanvas);

    startPoint = {
        x: cloud.offsetWidth / 2,
        y: cloud.offsetHeight / 2
    };

    wordsDown = [];
    callback();
}

/* =======================  PLACEMENT FUNCTIONS =======================  */
function createWordObject(word, freq) {
    var wordContainer = document.createElement("div");
    wordContainer.style.position = "absolute";
    // Hithesh
    if (freq * 50 < 0.00012) {
        freq = 10;
        wordContainer.style.fontSize = freq;
    } else {
        freq *= 50;
        wordContainer.style.fontSize = freq;
    }

    // Hithesh
    wordContainer.style.lineHeight = config.lineHeight;
    angle = Math.random() * (90 - 0) + 0;
    console.log(angle);
    if (parseInt(angle) % 2 != 0) {
        angle = 90;
    }
    else {
        angle = 0;
    }
    // Hithesh
    wordContainer.style.webkitTransform = 'rotate(' + angle + 'deg)';
    wordContainer.appendChild(document.createTextNode(word));
    return wordContainer;
}

function placeWord(word, x, y) {
    cloud.appendChild(word);
    word.style.left = x - word.offsetWidth / 2 + "px";
    word.style.top = y - word.offsetHeight / 2 + "px";
    wordsDown.push(word.getBoundingClientRect());
}

function trace(x, y) {
    traceCanvasCtx.fillRect(x, y, 1, 1);
}

function spiral(i, callback) {
    angle = config.spiralResolution * i;
    x = (1 + angle) * Math.cos(angle);
    y = (1 + angle) * Math.sin(angle);
    return callback ? callback() : null;
}

function intersect(word, x, y) {
    cloud.appendChild(word);
    word.style.left = x - word.offsetWidth / 2 + "px";
    word.style.top = y - word.offsetHeight / 2 + "px";
    var currentWord = word.getBoundingClientRect();
    cloud.removeChild(word);
    for (var i = 0; i < wordsDown.length; i += 1) {
        var comparisonWord = wordsDown[i];
        if (!(currentWord.right + config.xWordPadding < comparisonWord.left - config.xWordPadding ||
            currentWord.left - config.xWordPadding > comparisonWord.right + config.wXordPadding ||
            currentWord.bottom + config.yWordPadding < comparisonWord.top - config.yWordPadding ||
            currentWord.top - config.yWordPadding > comparisonWord.bottom + config.yWordPadding)) {
            return true;
        }
    }
    return false;
}


// Generate Cloud based on user request
function generateWordCloud(wordlist, freqList, callback) {

    tmp = [];
    wordsDown = []
    for (i = 0; i < freqList.length; i++) {
        tmp.push(parseFloat(freqList[i]));
    }

    max = Math.max.apply(Math, tmp);
    min = Math.min.apply(Math, tmp);

    for (i = 0; i < tmp.length; i++) {
        tmp[i] = parseFloat(normalize(tmp[i], max, min));
    }
    var cloud = document.getElementById("word-cloud");
    cloud.innerHTML = "";

    // Hithesh
    initialSetup(function () {

        var words = wordlist.map(function (word, idx) {
            return {
                word: word,
                freq: tmp[idx]
            }
        })
        words.sort(function (a, b) {
            return -1 * (a.freq - b.freq);
        });

        // Dilip
        for (var i = 0; i < words.length; i += 1) {
            var word = createWordObject(words[i].word, words[i].freq);
            word.setAttribute('data-toggle', 'tooltip');
            word.className = "mytooltip";
            word.title = word.childNodes[0].nodeValue;
            for (var j = 0; j < config.spiralLimit; j++) {
                if (spiral(j, function () {
                    if (!intersect(word, startPoint.x + x + 20, startPoint.y + 20 + y)) {
                        placeWord(word, startPoint.x + x + 20, startPoint.y + 20 + y);
                        return true;
                    }
                })) {
                    break;
                }
            }
        }

        callback();

    });
}

// Hithesh
function normalize(val, max, min) {
    return (val - min) / (max - min);
}


// Dilip
function changeSubsequent(type) {
    let words = wordlistt["data"][type];
    let freq = wordlistt["data"][type + "_freq"];
    document.getElementById("loader").style.display = "block";
    generateWordCloud(words, freq, function () {
        $('#loader').removeClass();

    });

}

// Dilip
function selectType(type) {
    this.type = type;

}


// Dilip
function change_mode() {
    initialSetup(function () {
        var rqst = new XMLHttpRequest();
        $('#loader').addClass("loading style-2");
        rqst.open("POST", '/generate/', true);
        rqst.setRequestHeader("Content-Type", "application/json");
        rqst.onreadystatechange = function (data) {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {

                if (JSON.parse(rqst.response)["data"][type].length == 0) {
                    alert("Sorry! Could not find any Movie matching the given criteria");
                }

                wordlistt = JSON.parse(rqst.response);
                wordlist = JSON.parse(rqst.response)["data"][type];
                freqList = JSON.parse(rqst.response)["data"][type + "_freq"];
                generateWordCloud(wordlist, freqList, function () {
                    $('#loader').removeClass();

                });
            }
        }
        rqst.send(JSON.stringify({ "range": year, "genre": genre, "query_type": type, "num_words": noOfWords }));
    });
}