function dibujar_circulo(tx,ty, color)
{
    var c = document.getElementById("my_canvas");
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.arc(tx,ty,7,0,(Math.PI/180)*360,true);
    ctx.fillStyle= color;
    ctx.fill();
    ctx.stroke();
}

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    return [x,y]

}

function dibujar_desde_lista(lista1)
{
    var color = "#008000";

    for(var i= 0; i < lista1.length; i++)
    {
        dibujar_circulo(lista1[i][0], lista1[i][1], color);
    }
}

function lineas_desde_lista(lista1)
{
    var c = document.getElementById("my_canvas");
    var ctx = c.getContext("2d");
    ctx.strokeStyle = "rgb(200,0,0)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(lista1[0][0], lista1[0][1]);
    for(var i= 1; i < lista1.length; i++)
    {
        ctx.lineTo(lista1[i][0], lista1[i][1]);
        ctx.stroke();
    }
    ctx.lineTo(lista1[0][0], lista1[0][1]);
    ctx.stroke();
}

function dibujar_cir_reset(lista1, posicion)
{
    var color = "#008000";
    var color2= "#4682b4";
    for(var i= 0; i < lista1.length; i++)
    {
        if (i == posicion)
        {
            dibujar_circulo(lista1[i][0], lista1[i][1], color2);
        }
        else
        {
            dibujar_circulo(lista1[i][0], lista1[i][1], color);
        }
    }
}


function reinicio( posicion, estado)
{
    let img = document.querySelector('#ori_img');
    let canvas1 = document.getElementById('my_canvas');
    let new_width = img.width;
    let new_height = img.height;
    let ctx = canvas1.getContext('2d');
    if (img.width > 500 || img.height > 500)
    {
        let value = img.width > img.height? 500/img.width : 500/img.height;
        new_width = img.width * value;
        new_height = img.height * value;
        canvas1.width = new_width;
        canvas1.height = new_height;
    }
    else
    {
        canvas1.width = new_width;
        canvas1.height = new_height;
    }

    canvas1.getContext('2d').drawImage(img, 0, 0,new_width, new_height);


    if(estado)
    {
        dibujar_cir_reset(corners_image, posicion);
    }
    else
    {
        dibujar_desde_lista(corners_image);
        lineas_desde_lista(corners_image);
    }

}


let img = document.querySelector('#ori_img');
let canvas1 = document.getElementById('my_canvas');
let new_width = 0;
let new_height = 0;
console.log(img.src);
var image_helper = new Image();
image_helper.onload=function(){
          if (canvas1.getContext)
          {
            let ctx = canvas1.getContext('2d');
            new_width = img.width;
            new_height = img.height;
            if (img.width > 500 || img.height > 500)
            {
                let value = img.width > img.height? 500/img.width : 500/img.height;
                new_width = img.width * value;
                new_height = img.height * value;
                canvas1.width = new_width;
                canvas1.height = new_height;
            }
            else
            {
                canvas1.width = new_width;
                canvas1.height = new_height;
            }
          }
    canvas1.getContext('2d').drawImage(img, 0, 0,new_width, new_height);

}
image_helper.src = img.src;

img.onerror=function(){
    console.log("Fallo");
}

let estado = false;
let k_pos = 0;
const canvas = document.getElementById('my_canvas');

my_canvas.addEventListener("click", function(event)
{
    estado = !estado;
    const point_s = getCursorPosition(canvas, event);

    if (estado)
    {
        var distancia_min = 1000.0;
        for(var i = 0; i < corners_image.length; i++)
        {
           const dis = Math.sqrt(Math.pow(corners_image[i][0]-point_s[0], 2) + Math.pow(corners_image[i][1]-point_s[1],2))
           if(dis < distancia_min)
           {
               distancia_min = dis;
               k_pos = i;
           }
        }

        if(distancia_min < 10)
        {
            var c = document.getElementById("my_canvas");
            c.width=c.width;
            reinicio(k_pos, estado);
        }
    }
    else
    {

        corners_image[k_pos] = point_s;
        var c = document.getElementById("my_canvas");
        c.width=c.width;
        reinicio(k_pos, estado);
    }


},false);



