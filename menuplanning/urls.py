from django.urls import path
from . import views

app_name = 'menuplanning'


urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('confirm-save-cart/', views.confirm_save_cart, name='confirm_save_cart'), 
    path('saved-menu-plans/', views.saved_menu_planning_page, name='saved_menu_planning_page'),
    path('reset-saved-menus/', views.reset_saved_menus, name='reset_saved_menus'),
    path('api/warungs/', views.warungs_list, name='warungs_list'),
    path('api/menus/<str:warung>/', views.get_menus_by_warung, name='get_menus_by_warung'), 
    path('api/load-cart/', views.load_cart, name='load_cart'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
]