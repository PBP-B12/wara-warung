from django.urls import path
from authenticationdummy.views import login, register

app_name = 'authentication'

urlpatterns = [
    path('logind/', login, name='login'),
    path('registerd/', register, name='register'),
]