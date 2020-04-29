// by Chtiwi Malek ===> CODICODE.COM
var mousePressed = false;
var lastX, lastY;
var ctx;

function InitThis() {
    ctx = document.getElementById('myCanvas').getContext("2d");
    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    $('#myCanvas').mouseup(function (e) {
        if (mousePressed) {
            mousePressed = false;
            cPush();
        }
    });

    $('#myCanvas').mouseleave(function (e) {
        if (mousePressed) {
            mousePressed = false;
            cPush();
        }
    });
    drawImage();
}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        //ctx.globalCompositeOperation = 'source-out';
        ctx.strokeStyle = $('#selColor').val();
        ctx.lineWidth = $('#selWidth').val();
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x;
    lastY = y;
}

var cPushArray = new Array();
var cStep = -1;

function cPush() {
    cStep++;
    if (cStep < cPushArray.length) { cPushArray.length = cStep; }
    cPushArray.push(document.getElementById('myCanvas').toDataURL());
    document.title = cStep + ":" + cPushArray.length;
}
function cUndo() {
    if (cStep > 0) {
        cStep--;
        var canvasPic = new Image();
        canvasPic.src = cPushArray[cStep];
        canvasPic.onload = function () { ctx.drawImage(canvasPic, 0, 0); }
        document.title = cStep + ":" + cPushArray.length;
    }
}
function cRedo() {
    if (cStep < cPushArray.length-1) {
        cStep++;
        var canvasPic = new Image();
        canvasPic.src = cPushArray[cStep];
        canvasPic.onload = function () { ctx.drawImage(canvasPic, 0, 0); }
        document.title = cStep + ":" + cPushArray.length;
    }
}


function saveImage() {
    var dataURL = document.getElementById('myCanvas').toDataURL();
    //s = new FormData();
    //s.append('image', toblob(document.getElementById('myCanvas').toDataURL()));
    console.log(dataURL);
    $.ajax({
        type: "POST",
        url: "/submit_mask",
        data: {'img64': dataURL},
        //processData : false,
        //contentType : "multipart/form-data", 
        // cache: false,
        // processData: false,
    }).done(function(o) {
        console.log('saved'); 
        // If you want the file to be visible in the browser 
        // - please modify the callback in javascript. All you
        // need is to return the url to the file, you just saved 
        // and than put the image in your browser.
    });
}

function toblob(stuff) {
    var g, type, bi, ab, ua, b, i;
    g = stuff.split(',');
    if (g[0].split('png')[1])
        type = 'png';
    else if (g[0].split('jpeg')[1])
        type = 'jpeg';
    else
        return false;
    bi = atob(g[1]);
    ab = new ArrayBuffer(bi.length);
    ua = new Uint8Array(ab);
    for (i = 0; i < bi.length; i++) {
        ua[i] = bi.charCodeAt(i);
    }
    b = new Blob([ua], {
        type: "image/" + type
    });
    return b;
}
