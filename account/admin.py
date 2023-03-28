from django.contrib import admin
from .models import *
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'thumbnail', 'publishedDate', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author')


class UserBookListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'review', 'favorites', 'status')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'book')

class BookStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name', 'slug')
    list_display_links = ('status_name',)
    search_fields = ('status_name',)


admin.site.register(UserBookList, UserBookListAdmin)
admin.site.register(BookStatus, BookStatusAdmin)
admin.site.register(Book, BookAdmin)

