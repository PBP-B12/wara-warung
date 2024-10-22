from django.urls import path
from menu.views import show_main

app_name = 'menu'

urlpatterns = [
    path('', show_main, name='show_main'),
]