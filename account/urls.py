from django.urls import path

from account.views import *

urlpatterns = [
    path('', MyBook.as_view(), name='home'),
    path('status/favorites', FavoritesBook.as_view(), name='favorites'),
    path('status/<slug:status_slug>/', SortedByStatusBook.as_view(), name='status')
]