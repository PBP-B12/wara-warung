from django.urls import path
from menu.views import show_main, edit_menu, delete_menu, add_menu, add_menu_ajax, show_xml, show_json, get_warungs, add_menu_flutter, edit_menu_flutter

app_name = 'menu'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('edit/<int:id>', edit_menu, name='edit_menu'),
    path('add/', add_menu, name='add_menu'),
    path('add-ajax/', add_menu_ajax, name='add_menu_ajax'),
    path('delete/<int:id>', delete_menu, name='delete_menu'),
    path('get-warungs/', get_warungs, name="get_warungs"),
    path('add-menu-flutter/', add_menu_flutter, name="add_menu_flutter"),
    path('edit-menu-flutter/<int:id>/', edit_menu_flutter, name="edit_menu_flutter")
]