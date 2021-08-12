from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .utils import *
from .Google_API.send_email import enviar_email
import time


def index_vista(request):
    if request.method == 'POST':
        my_file = request.FILES['Original']
        archivo = (os.path.splitext(my_file.name))
        nombre = archivo[0]
        ubication_image = MEDIA_ROOT + "/"+nombre
        if os.path.isdir(ubication_image):
            shutil.rmtree(ubication_image)
            time.sleep(2)
        os.mkdir(ubication_image)
        fs = FileSystemStorage(location=ubication_image)
        filename = fs.save(my_file.name, my_file)
        return redirect(reverse('Ops:scanner_intro', kwargs={'name': nombre}))
    return render(request, 'Pages/Examen2/index_scanner.html')


def operators_2(request, name):
    path = MEDIA_ROOT + "/" + name
    values = get_original_file_extra(path, name)
    send_page = {}
    send_page['imagen'] = "/media/" + name + "/" + values
    send_page['camino'] = path
    send_page['nombre'] = values
    print(send_page)
    return render(request, 'Pages/Examen2/descentralizado1.html', send_page)


def get_corners(request, name):
    if request.method == 'POST':
        path = request.POST['camino']
        values = request.POST['nombre']
        estado, corners = solve_corners(path, values)
        if estado:
            return JsonResponse({
                'Estado': "OK",
                'esquinas1': [int(corners[0][0]), int(corners[0][1])],
                'esquinas2': [int(corners[1][0]), int(corners[1][1])],
                'esquinas3': [int(corners[2][0]), int(corners[2][1])],
                'esquinas4': [int(corners[3][0]), int(corners[3][1])],
            })
        else:
            return JsonResponse({'State': 'fail'})
    else:
        return JsonResponse({'State': 'fail'})


def make_scanner(request, name):
    if request.method == 'POST':
        path = request.POST['path']
        values = request.POST['name']
        esquinas = request.POST['esquinas']
        estado, image_color, image_gris, image_negro = get_image_perspective(path, values, esquinas)
        if estado:
            return JsonResponse({
                'Estado': "OK",
                'imagen_color': image_color,
                'imagen_gris': image_gris,
                'imagen_negro': image_negro,
            })
        else:
            return JsonResponse({'State': 'fail'})
    else:
        return JsonResponse({'State': 'fail'})


def contactanos(request):
    return render(request, 'Pages/Examen2/Contactanos.html')


def message_send(request):
    contenido = request.POST['message_comment']
    if enviar_email(contenido):
        return JsonResponse({'State': 'OK'})
    else:
        return JsonResponse({'State': 'fail'})
