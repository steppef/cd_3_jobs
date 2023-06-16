from django.contrib import admin

from .models import Book, Tag


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
