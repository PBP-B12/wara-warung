from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import Menu
from .models import Wishlist

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)  # Get all items in user's wishlist
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})  # Direct path to wishlist.html


@login_required
def add_to_wishlist(request, menu_id):
    # Fetch the menu item based on the menu_id
    menu_item = get_object_or_404(Menu, id=menu_id)
    
    # Create or get the Wishlist object for the user and the menu item
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, menu=menu_item)
    
    # Redirect to the wishlist view after adding
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
