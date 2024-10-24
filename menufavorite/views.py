from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import Menu
from .models import Wishlist

@login_required
def add_to_wishlist(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    # Mencari apakah item sudah ada di wishlist pengguna
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, menu=menu)

    if created:
        # Jika item baru ditambahkan ke wishlist
        return redirect('wishlist')  # Arahkan ke halaman wishlist
    else:
        # Jika item sudah ada di wishlist, tetap arahkan ke wishlist
        return redirect('wishlist')

@login_required
def remove_from_wishlist(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    Wishlist.objects.filter(user=request.user, menu=menu).delete()  # Menghapus dari wishlist
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)  # Mengambil semua item wishlist pengguna
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
