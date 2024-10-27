from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:menu_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:menu_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add-section/', views.add_section, name='add_section'),  # Add section URL
    path('section/delete/<int:section_id>/', views.delete_section, name='delete_section'),  # Delete section
    path('assign-section/<int:item_id>/', views.assign_section_to_wishlist_item, name='assign_section_to_wishlist_item'),
    path('update-section-name/<str:section_name>/', views.update_section_name, name='update_section_name'),
]
