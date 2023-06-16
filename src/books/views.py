import uuid

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Book, Tag


class BookCreateView(View):
    def get(self, request):
        Tag.objects.create(name='Tag-{}'.format(uuid.uuid4().hex))

        my_list = []
        my_list[1]

        Book.objects.create(title=f'Title-{uuid.uuid4().hex}', text=f'Title={uuid.uuid4().hex}')

        return HttpResponse('<h1>SUCCESS!</h1>')
