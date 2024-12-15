from django.urls import path
from search.views import search_menu, menu_data_flutter

app_name = 'search'

urlpatterns = [
    path('search-menu/', search_menu, name='search_menu'),
    path('menu-data/', menu_data_flutter, name='menu_data_flutter'),
]