from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.db.models import Avg
from menuplanning.models import Cart, CartItem, ChosenMenu
from menu.models import Menu
from warung.models import Warung
from ratereview.models import Review

# Helper function to get or create the user's cart
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(
        user=user,
        defaults={
            'name': f"{user.username}'s Cart",
            'budget': 100000
        }
    )
    return cart

@login_required(login_url='/login')
def show_main(request):
    cart = get_user_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)
    total_price = sum(item.quantity * item.item_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_name': cart.name,
    }
    return render(request, 'menuplanning/menuplanning.html', context)

def warungs_list(request):
    warungs = Warung.objects.all().values('id', 'nama')
    return JsonResponse({'warungs': list(warungs)})

def get_menus_by_warung(request, warung):
    menus = Menu.objects.filter(warung=warung).values('id', 'menu', 'harga', 'gambar', 'warung')
    
    # Add average rating to each menu item
    menus_with_ratings = []
    for menu in menus:
        avg_rating = Review.objects.filter(menu_id=menu['id']).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        menu_with_rating = {
            'id': menu['id'],
            'menu': menu['menu'],
            'harga': menu['harga'],
            'gambar': menu['gambar'],
            'warung': menu['warung'],
            'avg_rating': round(avg_rating, 1)  # Rounding for display
        }
        menus_with_ratings.append(menu_with_rating)
    
    return JsonResponse({'menus': menus_with_ratings})

@login_required
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        budget = int(request.POST.get('budget'))

        cart = get_user_cart(request.user)
        menu_item = get_object_or_404(Menu, id=item_id)
        item_name = menu_item.menu
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item_name=item_name,
            defaults={'quantity': quantity, 'item_price': price}
        )

        if not created:
            cart_item.quantity = quantity
            cart_item.item_price = price
            cart_item.save()

        cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)
        total_price = sum(item.quantity * item.item_price for item in cart_items)
        item_count = sum(item.quantity for item in cart_items)
        exceeded_budget = total_price > budget

        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': cart_items})

        return JsonResponse({
            'updated_cart_html': updated_cart_html,
            'total_price': total_price,
            'item_count': item_count,
            'exceeded_budget': exceeded_budget
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
@csrf_exempt
def confirm_save_cart(request):
    if request.method == 'POST':
        budget = int(request.POST.get('budget', 100000))
        cart = get_user_cart(request.user)
        cart_items = CartItem.objects.filter(cart=cart).exclude(quantity=0)
        
        total_price = sum(item.quantity * item.item_price for item in cart_items)

        if total_price > budget:
            return JsonResponse({'error': 'Cannot save; budget exceeded.'}, status=400)

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

        cart_items.update(quantity=0)
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': []})
        
        return JsonResponse({
            'message': 'Cart saved successfully', 
            'updated_cart_html': updated_cart_html, 
            'total_price': 0
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def saved_menu_planning_page(request):
    chosen_menus = ChosenMenu.objects.filter(user=request.user).exclude(quantity=0)
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
        ChosenMenu.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
@csrf_exempt
def empty_cart(request):
    if request.method == 'POST':
        user_cart = get_user_cart(request.user)
        CartItem.objects.filter(cart=user_cart).update(quantity=0)
        
        updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': []})
        return JsonResponse({
            'success': True,
            'message': 'Cart has been emptied.',
            'updated_cart_html': updated_cart_html,
            'total_price': 0
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def load_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).exclude(quantity=0)
    total_price = sum(item.quantity * item.item_price for item in cart_items)
    
    updated_cart_html = render_to_string('menuplanning/cart_items.html', {'cart_items': cart_items})
    
    return JsonResponse({
        'updated_cart_html': updated_cart_html,
        'total_price': total_price,
    })
