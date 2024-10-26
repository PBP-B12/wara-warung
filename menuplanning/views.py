from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from menuplanning.models import Cart, CartItem, ChosenMenu
from django.template.loader import render_to_string
from django.utils import timezone
from menu.models import Menu
from warung.models import Warung
from django.shortcuts import get_object_or_404


# Helper function to get or create the user's cart
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(
        user=user,
        defaults={
            'name': f"{user.username}'s Cart",  # Optional default name
            'budget': 100000  # Set a budget
        }
    )
    return cart


@login_required
def show_main(request):
    cart = get_user_cart(request.user)
    # Filter out items with quantity 0
    cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)

    # Calculate total cart price based on chosen items
    total_price = sum(item.quantity * item.item_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_name': cart.name,
    }
    return render(request, 'menuplanning/menuplanning.html', context)

def get_warungs(request):
    warungs = list(Warung.objects.values('id', 'nama'))
    return JsonResponse({'warungs': warungs})


def menu_list(request):
    menus = Menu.objects.all().values('id', 'menu', 'harga', 'gambar', 'warung')
    return JsonResponse({'menus': list(menus)}, safe=False)

def menus_by_warung(request, warung_id):
    menus = Menu.objects.filter(warung=warung_id).values('id', 'menu', 'harga', 'gambar', 'warung')
    return JsonResponse({'menus': list(menus)}, safe=False)


@login_required
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        budget = int(request.POST.get('budget'))  # Budget received from the frontend

        # Retrieve or create the user's cart
        cart = get_user_cart(request.user)

        # Get the menu item to retrieve the item name
        menu_item = get_object_or_404(Menu, id=item_id)
        item_name = menu_item.menu  # Retrieve the menu name for display

        # Get or create the cart item with the correct quantity and price
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item_name=item_name,
            defaults={'quantity': quantity, 'item_price': price}
        )

        # Update quantity and price if the item already exists
        if not created:
            cart_item.quantity = quantity
            cart_item.item_price = price
            cart_item.save()

        # Calculate the total price of items in the cart
        cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)
        total_price = sum(item.quantity * item.item_price for item in cart_items)

        # Render the updated cart items and check if total exceeds the budget
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': cart_items})
        exceeded_budget = total_price > budget

        return JsonResponse({
            'updated_cart_html': updated_cart_html,
            'total_price': total_price,
            'exceeded_budget': exceeded_budget
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
@csrf_exempt
def save_cart(request):
    if request.method == 'POST':
        cart = get_user_cart(request.user)
        cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)
        budget = int(request.POST.get('budget', 100000))

        # Calculate total cart price
        total_price = sum(item.quantity * item.item_price for item in cart_items)

        # If over budget, render the confirm popup with an error message
        if total_price > budget:
            error_message = render_to_string('menuplanning/confirm.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'cart_name': cart.name,
                'budget': budget,
                'exceeded_budget': True
            })
            return JsonResponse({'saved_cart_html': error_message, 'error': 'Budget exceeded!'}, status=400)

        # Render confirmation popup without saving items to ChosenMenu
        confirm_popup_html = render_to_string('menuplanning/confirm.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_name': cart.name,
            'budget': budget,
            'exceeded_budget': False
        })

        return JsonResponse({'confirm_popup_html': confirm_popup_html})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



# Untuk nunjukkin popup message confirm.html
def save_cart_view(request):
    return render(request, 'confirm.html')


@login_required
def saved_menu_planning_page(request):
    chosen_menus = ChosenMenu.objects.filter(user=request.user).exclude(quantity=0)

    # Organize menu plans by save_session
    menu_plans_dict = {}
    for menu in chosen_menus:
        if menu.save_session not in menu_plans_dict:
            menu_plans_dict[menu.save_session] = {
                'name': f"Menu Planning {menu.save_session}",
                'budget': menu.budget,
                'items': [],
                'total_price': 0,
            }

        item_total = menu.quantity * menu.price
        menu_plans_dict[menu.save_session]['total_price'] += item_total
        menu_plans_dict[menu.save_session]['items'].append({
            'item_name': menu.item_name,
            'quantity': menu.quantity,
            'price': menu.price,
            'total': item_total
        })

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

from django.template.loader import render_to_string

@login_required
@csrf_exempt
def confirm_save_cart(request):
    if request.method == 'POST':
        budget = int(request.POST.get('budget', 100000))
        cart = get_user_cart(request.user)
        cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)
        
        # Calculate the total price again for a final check
        total_price = sum(item.quantity * item.item_price for item in cart_items)

        # If total price exceeds the budget, return an error (in case budget changed)
        if total_price > budget:
            return JsonResponse({'error': 'Cannot save; budget exceeded.'}, status=400)

        # Save items to ChosenMenu
        save_session_id = int(timezone.now().timestamp())
        for item in cart_items:
            ChosenMenu.objects.create(
                user=request.user,
                item_name=item.item_name,
                quantity=item.quantity,
                price=item.item_price,
                save_session=save_session_id,
                budget=budget
            )

        # Reset cart items after saving
        cart_items.update(quantity=0)

        # Render an empty cart for the frontend
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': []})
        
        return JsonResponse({
            'message': 'Cart saved successfully', 
            'updated_cart_html': updated_cart_html, 
            'total_price': 0
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def menu_list(request, warung_id):
    # Filter menus based on the warung_id
    menus = Menu.objects.filter(warung=warung_id)
    data = [
        {
            'menu': menu.menu,
            'harga': menu.harga,
            'warung': menu.warung,
            'gambar': menu.gambar,
            'id': menu.id,
        } for menu in menus
    ]
    return JsonResponse({'menus': data})

def get_menus_by_warung(request, warung):
    # Retrieve menus for the selected warung_id
    menus = Menu.objects.filter(warung=warung)

    # Prepare the data to be returned
    data = [
        {
            'menu': menu.menu,
            'harga': menu.harga,
            'warung': menu.warung,  # Include warung name
            'gambar': menu.gambar,
            'id': menu.id,
        }
        for menu in menus
    ]
    return JsonResponse({'menus': data})

def warungs_list(request):
    warungs = Warung.objects.all()
    data = {'warungs': [{'id': warung.id, 'nama': warung.nama} for warung in warungs]}
    return JsonResponse(data)

def get_warungs(request):
    warungs = Warung.objects.all().values('id', 'nama')
    return JsonResponse({'warungs': list(warungs)})

@login_required
@csrf_exempt
def empty_cart(request):
    if request.method == 'POST':
        # Get the user's cart and set all item quantities to zero
        user_cart = get_user_cart(request.user)
        CartItem.objects.filter(cart=user_cart).update(quantity=0)

        # Return a success message and reset cart HTML
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': []})
        return JsonResponse({
            'success': True,
            'message': 'Cart has been emptied.',
            'updated_cart_html': updated_cart_html,
            'total_price': 0
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)








