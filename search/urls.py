from django.urls import path
from search.views import search_menu

app_name = 'search'

urlpatterns = [
    path('', search_menu, name='search_menu'),
]