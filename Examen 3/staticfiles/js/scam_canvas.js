function draw(img)
{
  var canvas = document.getElementById('my_canvas');
  if (canvas.getContext)
  {
    var ctx = canvas.getContext('2d');
    canvas.width = img.width
    canvas.height = img.height
    ctx.drawImage(img, 0, 0,img.width, img.height);

  }
}

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

function reset()
{
    var c = document.getElementById("my_canvas");
    c.width=c.width;
}

function reinicio( posicion, estado)
{
    const img = document.querySelector('#ori_img')
    var c = document.getElementById("my_canvas");
    var ctx = c.getContext("2d");
    ctx.drawImage(img, 0, 0,img.width, img.height)
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
