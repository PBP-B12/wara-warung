from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, ChosenMenu
from django.template.loader import render_to_string
from django.utils import timezone
from menu.models import Menu

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

        # Get the user's cart
        cart = get_user_cart(request.user)

        # Get or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item_name=item_id,
            defaults={'quantity': quantity, 'item_price': price}
        )

        # Update the quantity and price if the item already exists
        if not created:
            cart_item.quantity = quantity
            cart_item.item_price = price
            cart_item.save()

        # Fetch only items with quantity > 0
        cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)

        # Calculate the updated total price
        total_price = sum(item.quantity * item.item_price for item in cart_items)

        # Render the updated cart HTML
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': cart_items})

        return JsonResponse({
            'updated_cart_html': updated_cart_html,
            'total_price': total_price
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
@csrf_exempt
def save_cart(request):
    cart = get_user_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)  # Exclude items with zero quantity
    budget = int(request.POST.get('budget', 100000))

    for item in cart_items:
        item.total_price = item.quantity * item.item_price

    total_price = sum(item.total_price for item in cart_items)

    if total_price > budget:
        error_message = render_to_string('menuplanning/confirm.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_name': cart.name,
            'budget': budget,
            'exceeded_budget': True
        })
        return JsonResponse({'saved_cart_html': error_message, 'error': 'Budget exceeded!'}, status=400)

    saved_cart_html = render_to_string('menuplanning/confirm.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_name': cart.name,
        'budget': budget,
    })

    return JsonResponse({'saved_cart_html': saved_cart_html})



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

@login_required
@csrf_exempt
def confirm_save_cart(request):
    if request.method == 'POST':
        budget = request.POST.get('budget')
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        user_budget = float(budget) if budget else 100000
        save_session_id = int(timezone.now().timestamp())

        # Save the current cart items to the ChosenMenu model
        for item in cart_items:
            ChosenMenu.objects.create(
                user=request.user,
                item_name=item.item_name,
                quantity=item.quantity,
                price=item.item_price,
                save_session=save_session_id,
                budget=user_budget
            )

        # Reset cart item quantities to zero and update the price
        cart_items.update(quantity=0)

        return JsonResponse({'message': 'Cart saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)








