from django.contrib.auth.views import PasswordResetView
from django.urls import path

from auth_and_reg.views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

]
