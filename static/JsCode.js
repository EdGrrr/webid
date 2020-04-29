// by Chtiwi Malek ===> CODICODE.COM
var mousePressed = false;
var lastX, lastY;
var ctx;
var deleting = false;
var delX = -1;
var delY = -1;
var lineDrawing = false;
var lineX = -1;
var lineY = -1;

function InitThis() {
    ctx = document.getElementById('myCanvas').getContext("2d");
    $('#myCanvas').mousedown(function (e) {
        if (deleting) {
            if (delX >= 0) {
                //Delete the box
                ctx.clearRect(delX,delY,
                              e.pageX - $(this).offset().left - delX,
                              e.pageY - $(this).offset().top - delY);
                delX = -1;
                delY = -1;
            }
            else {
                delX = e.pageX - $(this).offset().left;
                delY = e.pageY - $(this).offset().top;
                console.log(delX);
                console.log(delY);
            }
        } else if (lineDrawing) {
            if (lineX >= 0) {
                //Delete the box
                lineX = -1;
                lineY = -1;
            }
            else {
                lineX = e.pageX - $(this).offset().left;
                lineY = e.pageY - $(this).offset().top;
                console.log(lineX);
                console.log(lineY);
            }
        } else {
            mousePressed = true;
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
        }
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

    
    drawImage(); //Defined on template to get mask correct
}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.globalCompositeOperation = 'destination-atop';
        ctx.strokeStyle = 'red';
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
    console.log(dataURL);
    $.ajax({
        type: "POST",
        url: "/submit_mask",
        data: {'img64': dataURL},
    }).done(function(o) {
        console.log('saved'); 
        // If you want the file to be visible in the browser 
        // - please modify the callback in javascript. All you
        // need is to return the url to the file, you just saved 
        // and than put the image in your browser.
    });
}


// Shortcuts
// d - deleteing mode (draw boxes with two clicks
// t - toggle mask
// l - line drawing mode
// p - polgon drawing mode
$(document).keypress(function (e) {
    console.log(e.which);
    if(e.which == 100 ) {
        deleting = !deleting;
        delX = -1;
        delY = -1;
        console.log(deleting);
    } else if (e.which == 116 ) {
        $('#myCanvas').toggle();
    } else if (e.which == 108) {
        lineDrawing = !lineDrawing;
        lineX = -1;
        lineY = -1;
    }
});
