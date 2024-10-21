from django.urls import path
from warung.views import show_main, show_warung

app_name = 'warung'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('<str:namawarung>', show_warung, name='show_warung'),
]