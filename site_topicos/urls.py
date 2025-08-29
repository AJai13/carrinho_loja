from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def index(request):
    print('')
    return HttpResponse("Adicione ' /loja/ ' ao final da URL para navegar na lojinha!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('loja/', include('loja.urls')),
    path('', index),
]
