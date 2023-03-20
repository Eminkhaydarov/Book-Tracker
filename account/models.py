from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pages = models.IntegerField()
    thumbnail = models.URLField()
    publishedDate = models.DateField()


class UserBookList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.PROTECT)
    status = models.ForeignKey('StatusBook', on_delete=models.PROTECT)
    review = models.TextField()


class StatusBook(models.Model):
    name = models.CharField(max_length=255)
