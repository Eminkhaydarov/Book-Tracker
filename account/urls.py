from django.urls import path

from account.views import *

urlpatterns = [
    path('', MyBook.as_view(), name='home'),
    path('status/favorites', FavoritesBookView.as_view(), name='favorites'),
    path('status/<slug:status_slug>/', SortedByStatusBookView.as_view(), name='status'),
    path('add_book', add_book, name='add_book'),
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('delete_book/<slug:slug>/', DeleteBookView.as_view(), name='delete'),
    path('update_book/<slug:slug>/', update_book, name='update_book')
]
