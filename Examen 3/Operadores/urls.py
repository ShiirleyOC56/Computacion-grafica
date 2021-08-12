from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import vistas_scanner
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'Ops'

urlpatterns = [
    path('', views.index, name='index'),
    path('loginfirebase', views.login, name='login'),
    path('indexlogin', views.indexlogin, name='indexlogin'),
    path('mod_scanner/', vistas_scanner.index_vista, name='scanner_index'),
    path('contactanos/', vistas_scanner.contactanos, name='contactanos'),
    path('contactanos/send_message/', vistas_scanner.message_send),
    path('mod_scanner/<str:name>', vistas_scanner.operators_2, name='scanner_intro'),
    path('mod_scanner/<str:name>/corners', vistas_scanner.get_corners),
    path('mod_scanner/<str:name>/scanner', vistas_scanner.make_scanner),
    path('img/<str:name>', views.operators, name='operators'),
    path('img/<str:name>/data_thresholding', views.image_thresholding),
    path('img/<str:name>/data_contrast', views.image_contrast_streching),
    path('img/<str:name>/data_equalization', views.image_histogram_equalization),
    path('img/<str:name>/data_exponential', views.image_exponential),
    path('img/<str:name>/data_logarithm', views.image_logarithm),
    path('img/<str:name>/data_square', views.image_square_root),
    path('img/<str:name>/data_pow', views.image_raise_power),
    path('img/<str:name>/data_addition', views.image_addition),
    path('img/<str:name>/data_difference', views.image_difference),
    path('img/<str:name>/data_dot', views.image_dot),
    path('img/<str:name>/data_division', views.image_division),
    path('img/<str:name>/data_blending', views.image_blending),
    path('img/<str:name>/data_AND', views.image_AND),
    path('img/<str:name>/data_OR', views.image_OR),
    path('img/<str:name>/data_XOR', views.image_XOR),
    path('img/<str:name>/up_image', views.up_image),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
