from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)


class Tag(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
