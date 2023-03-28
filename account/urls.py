from django.urls import path

from account.views import MyBook

urlpatterns = [
    path('', MyBook.as_view(), name='home')
]