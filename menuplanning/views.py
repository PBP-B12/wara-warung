from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, ChosenMenu
from django.template.loader import render_to_string

# Helper function to get or create the user's cart
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# Main view to display the menu planning page
@login_required
def show_main(request):
    cart = get_user_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price for each item
    for item in cart_items:
        item.total_price = item.quantity * item.item_price

    # Calculate total cart price
    total_price = sum(item.total_price for item in cart_items)

    # Pass the cart items and total price to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_name': cart.name,  # Ensure you pass cart_name here
    }
    return render(request, 'menuplanning/menuplanning.html', context)



@login_required
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))

        # Get the user's cart
        cart = get_user_cart(request.user)

        # Try to get the cart item, or create a new one if it doesn't exist
        try:
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
        except CartItem.DoesNotExist:
            # If the item doesn't exist in the cart, create a new cart item
            cart_item = CartItem.objects.create(cart=cart, id=item_id, quantity=quantity, item_price=price)

        # Update the quantity and save the cart item
        cart_item.quantity = quantity
        cart_item.save()

        # Fetch the updated cart items
        cart_items = CartItem.objects.filter(cart=cart)

        # Calculate the updated total price for the cart
        total_price = sum(item.quantity * item.item_price for item in cart_items)

        # Render the updated cart items HTML
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': cart_items})

        # Return the updated cart HTML and total price in the response
        return JsonResponse({
            'updated_cart_html': updated_cart_html,
            'total_price': total_price
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
@csrf_exempt
def save_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price for each item and pass to template
    for item in cart_items:
        item.total_price = item.quantity * item.item_price

    total_price = sum(item.total_price for item in cart_items)

    if total_price > 100000:
        error_message = render_to_string('menuplanning/confirm.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_name': cart.name,
            'budget': cart.budget,
            'exceeded_budget': True
        })
        return JsonResponse({'saved_cart_html': error_message, 'error': 'Budget exceeded!'}, status=400)

    saved_cart_html = render_to_string('menuplanning/confirm.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_name': cart.name,
        'budget': cart.budget,
    })

    return JsonResponse({'saved_cart_html': saved_cart_html})

# Untuk nunjukkin popup message confirm.html
def save_cart_view(request):
    return render(request, 'confirm.html')


@login_required
@csrf_exempt
def confirm_save_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart.is_saved = True
        cart.save()
        return JsonResponse({'message': 'Cart saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



# @login_required
# def saved_menu_planning_page(request):
#     chosen_menus = ChosenMenu.objects.filter(user=request.user)  # Filter for menus saved by the logged-in user
#     context = {
#         'chosen_menus': chosen_menus,
#     }
#     return render(request, 'menuplanning/saved_menu_plans.html', context)

# @login_required
# def saved_menu_planning_page(request):
#     chosen_menus = ChosenMenu.objects.filter(user=request.user)  # Retrieve all saved items for the user
    
#     # Organize the menu items and calculate totals
#     items = []
#     total_price = 0

#     for item in chosen_menus:
#         item_total = item.quantity * item.price
#         total_price += item_total
#         items.append({
#             'item_name': item.item_name,
#             'quantity': item.quantity,
#             'price': item.price,
#             'total': item_total
#         })

#     # Add all items to a single menu plan dictionary
#     menu_plan = {
#         'name': "Saved Menu Plan",  # Static name or customize as needed
#         'budget': 100000,           # Set or retrieve your budget here
#         'items': items,
#         'total_price': total_price
#     }

#     return render(request, 'menuplanning/saved_menu_plans.html', {'menu_plans': [menu_plan]})

@login_required
def saved_menu_planning_page(request):
    # Retrieve all saved menus grouped by session
    chosen_menus = ChosenMenu.objects.filter(user=request.user)
    
    # Use a dictionary to group items by each unique saving session
    menu_plans_dict = {}
    for menu in chosen_menus:
        # Assume each 'menu.save_session' is a unique identifier for saved sessions
        if menu.save_session not in menu_plans_dict:
            menu_plans_dict[menu.save_session] = {
                'name': f"Menu Planning {menu.save_session}",  # Unique name per session
                'budget': 100000,  # Set budget here or dynamically
                'items': [],
                'total_price': 0,
            }
        
        # Calculate the total for each item and add it to the corresponding session plan
        item_total = menu.quantity * menu.price
        menu_plans_dict[menu.save_session]['total_price'] += item_total
        menu_plans_dict[menu.save_session]['items'].append({
            'item_name': menu.item_name,
            'quantity': menu.quantity,
            'price': menu.price,
            'total': item_total
        })

    # Convert the dictionary to a list of menu plans for rendering
    menu_plans = list(menu_plans_dict.values())

    return render(request, 'menuplanning/saved_menu_plans.html', {'menu_plans': menu_plans})



@login_required
@csrf_exempt
def reset_saved_menus(request):
    if request.method == 'POST':
        # Delete all saved menus for the current user
        ChosenMenu.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


