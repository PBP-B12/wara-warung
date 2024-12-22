from django.urls import path
from . import views
from menuplanning import views
from .views import get_csrf_token

app_name = 'menuplanning'


urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('confirm-save-cart/', views.confirm_save_cart, name='confirm_save_cart'), 
    path('saved-menu-plans/', views.saved_menu_planning_page, name='saved_menu_planning_page'),
    path('reset-saved-menus/', views.reset_saved_menus, name='reset_saved_menus'),
    path('api/warungs/', views.warungs_list, name='warungs_list'),
    path('api/warungs/flutter/', views.warungs_list_flutter, name="warungs_list_flutter"),
    path('api/menus/<str:warung>/', views.get_menus_by_warung, name='get_menus_by_warung'), 
    path('api/menus/flutter/<str:warung>/', views.get_menus_by_warung_flutter, name='get_menus_by_warung_flutter'), 
    path('api/load-cart/', views.load_cart, name='load_cart'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('carts/json/', views.show_carts_json, name='show_carts_json'),
    path('cart-items/json/', views.show_cart_items_json, name='show_cart_items_json'),
    path('chosen-menus/json/', views.show_chosen_menus_json, name='show_chosen_menus_json'),
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('create-menu-flutter/', views.create_menu_flutter, name='create_menu_flutter'),
]