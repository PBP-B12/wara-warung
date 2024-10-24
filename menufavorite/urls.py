from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/', views.wishlist_view, name='wishlist'),  # Menampilkan wishlist pengguna
    path('wishlist/add/<int:menu_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Menambahkan ke wishlist
    path('wishlist/remove/<int:menu_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # Menghapus dari wishlist
]
