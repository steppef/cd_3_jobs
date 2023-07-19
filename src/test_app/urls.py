from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def test_view(request):
    for k, v in request.META.items():
        print(f'key: {k} | value: {v}')
        print(f'key: {k} | value: {v}')
        print(f'key: {k} | value: {v}')
    return HttpResponse(f'<h1>{request.__dict__}</h1>')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view),
    path('', include('books.urls'))
]
