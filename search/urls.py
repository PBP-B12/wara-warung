from django.urls import path
from search.views import search_menu

app_name = 'search'

urlpatterns = [
    path('search-menu/', search_menu, name='search_menu'),
]