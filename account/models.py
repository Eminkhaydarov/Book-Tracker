from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    thumbnail = models.URLField()
    publishedDate = models.DateField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

class UserBookList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.PROTECT)
    review = models.TextField(blank=True)
    favorites = models.BooleanField(default=False)
    status = models.ForeignKey('BookStatus', on_delete=models.PROTECT)


class BookStatus(models.Model):
    status_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.status_name

    def get_absolute_url(self):
        return reverse('status', kwargs={'status_slug': self.slug})

