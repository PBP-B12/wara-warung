# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist, Category, Menu
from .forms import CategoryForm
from django.http import JsonResponse  # Add this import
from django.template.loader import render_to_string  # Ensure render_to_string is imported here
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
    
@login_required
def wishlist_view(request):
    category_name = request.GET.get('category_name')
    categories = Category.objects.filter(user=request.user)

    # Filter wishlist items based on selected category
    if category_name:
        category = get_object_or_404(Category, name=category_name, user=request.user)
        wishlist_items = Wishlist.objects.filter(user=request.user, categories=category)
    else:
        wishlist_items = Wishlist.objects.filter(user=request.user)

    # Handle AJAX request for dynamic filtering
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        wishlist_html = render_to_string('partials/wishlist_items.html', {
            'wishlist_items': wishlist_items,
            'categories': categories  # Include categories in the context
        }, request=request)
        return JsonResponse({'wishlist_html': wishlist_html})

    # For non-AJAX requests, render the full wishlist page
    category_form = CategoryForm()
    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items,
        'categories': categories,
        'category_form': category_form,
        'selected_category': category_name,
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            # Check if the category already exists for the user
            category, created = Category.objects.get_or_create(
                name=category_name, user=request.user
            )
            if created:
                messages.success(request, 'Category added successfully.')
            else:
                messages.info(request, 'Category already exists.')

            # Check if the request is AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                categories = list(Category.objects.filter(user=request.user).values('id', 'name'))
                return JsonResponse({'categories': categories})

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid category name.'}, status=400)
            messages.error(request, 'Invalid category name.')
    
    return redirect('wishlist')

def assign_category_to_item(request, item_id):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        
        if category_id:
            wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
            category = get_object_or_404(Category, id=category_id, user=request.user)
            
            # Clear existing categories and add the selected category
            wishlist_item.categories.clear()
            wishlist_item.categories.add(category)

            # Return JSON response without messages
            response = {
                'status': 'success',
                'category_name': category.name  # Send the category name to update the UI
            }
            return JsonResponse(response)
        
        # Return JSON error response without messages
        return JsonResponse({'status': 'error', 'message': 'Please select a category.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
def add_to_wishlist(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, menu=menu_item)
    if created:
        messages.success(request, f'{menu_item.menu} added to your wishlist.')
    else:
        messages.info(request, f'{menu_item.menu} is already in your wishlist.')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, menu_id):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        menu_item = get_object_or_404(Menu, id=menu_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, menu=menu_item).first()

        if wishlist_item:
            wishlist_item.delete()
            response = {
                'status': 'success',
                'menu_id': menu_id,
                'message': f'{menu_item.menu} has been removed from your wishlist.'
            }
        else:
            response = {
                'status': 'error',
                'message': 'Item not found in wishlist.'
            }
        
        print("AJAX Response:", response)  # Debugging output for the server console
        return JsonResponse(response)
    
    # Redirect if not an AJAX request
    return redirect('wishlist')

@login_required  # Pastikan hanya pengguna yang login yang dapat mengakses API ini
def show_json(request):
    data = []
    
    # Filter hanya wishlist yang terkait dengan pengguna yang sedang login
    wishlists = Wishlist.objects.filter(user=request.user).select_related('user', 'menu').prefetch_related('categories')

    for wishlist in wishlists:
        data.append({
            'id': wishlist.id,
            'user': wishlist.user.username,
            'menu': {
                'id': wishlist.menu.id,
                'name': wishlist.menu.menu,  # Sesuaikan dengan field model Menu
                'harga': wishlist.menu.harga,
                'warung' : wishlist.menu.warung,
                'gambar' : wishlist.menu.gambar,
            },
            'categories': [
                {'id': category.id, 'name': category.name} 
                for category in wishlist.categories.all()
            ],
        })
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def remove_from_wishlist_flutter(request):
    if request.method == "POST":
        try:
            # Parsing JSON request body
            data = json.loads(request.body)
            menu_id = data.get("menu_id")

            if not menu_id:
                return JsonResponse(
                    {"status": "error", "message": "menu_id is required."},
                    status=400
                )

            # Mendapatkan menu item berdasarkan ID
            menu_item = get_object_or_404(Menu, id=menu_id)
            wishlist_item = Wishlist.objects.filter(user=request.user, menu=menu_item).first()

            if wishlist_item:
                wishlist_item.delete()
                response = {
                    "status": "success",
                    "menu_id": menu_id,
                    "message": f"{menu_item.menu} has been removed from your wishlist."
                }
            else:
                response = {
                    "status": "error",
                    "message": "Item not found in wishlist."
                }
            
            return JsonResponse(response, status=200)

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON format."},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"An error occurred: {str(e)}"},
                status=500
            )

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)