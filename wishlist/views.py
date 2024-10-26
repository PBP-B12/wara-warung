# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist, Category, Menu
from .forms import CategoryForm
from django.http import JsonResponse  # Add this import

@login_required
def wishlist_view(request):
    category_name = request.GET.get('category_name')  # Get the category filter from the query parameters
    categories = Category.objects.filter(user=request.user)

    # If a category is selected, filter the wishlist items by that category
    if category_name:
        category = get_object_or_404(Category, name=category_name, user=request.user)
        wishlist_items = Wishlist.objects.filter(user=request.user, categories=category)
    else:
        wishlist_items = Wishlist.objects.filter(user=request.user)

    category_form = CategoryForm()  # Form for adding new categories

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