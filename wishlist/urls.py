# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:menu_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Match /wishlist/add/<menu_id>/
    path('add-category/', views.add_category, name='add_category'),
    path('assign-category/<int:item_id>/', views.assign_category_to_item, name='assign_category_to_item'),
    path('wishlist/remove/<int:menu_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('json/', views.show_json, name='show_json'),
    path('remove-wishlist/', views.remove_from_wishlist_flutter, name='remove_from_wihslist_flutter'),
    path('allcategory/', views.show_all_categories, name="show_all_categories"),
    path('add-category-flutter/', views.add_category_flutter, name="add_category_flutter"),
    path('show_wishlist_by_category/', views.show_wishlist_by_category, name="show_wishlist_by_category"),
    path('assign_category_to_item_flutter/', views.assign_category_to_item_flutter, name="assign_category_to_item_flutter"),
    path('add_to_wishlist_flutter/', views.add_to_wishlist_flutter, name="add_to_wishlist_flutter")
] 