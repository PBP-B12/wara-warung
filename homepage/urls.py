from django.urls import path
from homepage.views import show_main, get_warungs

app_name = 'homepage'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('api/warungs/', get_warungs, name='get_warungs'),
]