from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def test_view(request):
    return HttpResponse('<h1>cdcdc asdasdasd tes msg</h1>')


urlpatterns = [
    path('adminnn/', admin.site.urls),
    path('test/', test_view)
]
