from django.urls import path
from . import views

app_name = 'menuplanning'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('save-cart/', views.save_cart, name='save_cart'),
    path('confirm-save-cart/', views.confirm_save_cart, name='confirm_save_cart'), 
    path('saved-menu-plans/', views.saved_menu_planning_page, name='saved_menu_planning_page'),
    path('reset-saved-menus/', views.reset_saved_menus, name='reset_saved_menus'),

]