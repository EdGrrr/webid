// by Chtiwi Malek ===> CODICODE.COM
var mousePressed = false;
var lastX, lastY;
var ctx;
var eraseX1, eraseY1, eraseX2, eraseY2;
var isErasing = false;
var drawState = 'paint'; //states: paint, erase, line, polygon
var lastState = 'paint';

function InitThis() {
    ctx = document.getElementById('myCanvas').getContext("2d");

    $('#erasingButton').mousedown(function (e) {
        toggleErase();
    });
    
    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        eraseX1 = e.pageX- $(this).offset().left;
        eraseY1 = e.pageY- $(this).offset().top;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            eraseX2 = e.pageX- $(this).offset().left;
            eraseY2 = e.pageY- $(this).offset().top;
            if (drawState=='paint') {
                Draw(eraseX2, eraseX1, true);
            }
        }
    });

    $('#myCanvas').mouseup(function (e) {
        if (mousePressed) {
            mousePressed = false;
            if (drawState=='erase') {
                erase();
            } else if (drawState=='line') {
                Draw(eraseX2, eraseY2, true);
            }
            cPush();
        }
    });

    $('#myCanvas').mouseleave(function (e) {
        if (mousePressed) {
            mousePressed = false;
            cPush();
        }
    });  


    $('#imageCompleteBtn').click(function (e) {
        //console.log($(this).data("image"))
        saveImage();
        var experiment = $(this).data("exp")
        var image_name = $(this).data("image");
        var image_notes = $('#imageNotes').val();
        var image_check = $('#imageCheck').is(':checked');
        // console.log(granule_notes);
        // console.log(granule_check);
        $.post( "/exp/"+experiment+"/image_complete/"+image_name, 
                {"image_data": JSON.stringify({
                    "checked": image_check,
                    "notes": image_notes,
                    "exp": experiment
                }),
                },
              );
    });
    
    drawImage(); //Defined on template to get mask correct
}

function erase() {
    const x = Math.min(eraseX1, eraseX2);
    const y = Math.min(eraseY1, eraseY2);
    const xx = Math.max(eraseX1, eraseX2);
    const yy = Math.max(eraseY1, eraseY2);
    const w = xx - x;
    const h = yy - y;
    ctx.clearRect(x, y, w, h);
}

function toggleErase() {
    if (drawState != 'erase') {
        lastState = drawState;
        drawState = 'erase';
    } else {
        drawState = lastState;
    }
}

function Draw(x, y, isDown) {
    if (isDown) {
        if ((drawState=='paint')|(drawState=='line')) {
            ctx.beginPath();
            ctx.imageSmoothingEnabled = false;
            ctx.strokeStyle = 'red';
            ctx.lineWidth = $('#selWidth').val();
            ctx.lineJoin = "round";
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(x, y);
            ctx.closePath();
            ctx.stroke();
        }
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
    var image_name = $('#imageOptions').data("image");
    console.log(dataURL);
    $.ajax({
        type: "POST",
        url: "/submit_mask/"+image_name,
        data: {'img64': dataURL},
    }).done(function(o) {
        console.log('saved'); 
    });
}


// Shortcuts
// d - deleting mode (draw boxes with two clicks)
// t - toggle mask
// l - line drawing mode
// p - polgon drawing mode
$(document).keypress(function (e) {
    console.log(e.which);
    if(e.which == 101 ) {
        //e - toggle erase box
        toggleErase();
        console.log(drawState);
    } else if (e.which == 116 ) {
        //t - toggle mask visibility
        $('#myCanvas').toggle();
    } else if (e.which == 108) {
        //l - set line drawing mode
        drawState = 'line';
    } else if (e.which == 100) {
        //d - set draw drawing mode
        drawState = 'paint';
    } else if (e.which == 112) {
        //p - set polygon drawing mode
        drawState = 'polygon';
    }
});
