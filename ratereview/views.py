from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from menu.models import Menu  # Import Menu from the other app
from ratereview.models import MenuRating, Review  # Adjust the import based on your app structure

def show_main(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)  # Fetch the menu item
    menu_rating, created = MenuRating.objects.get_or_create(menu=menu_item)  # Get or create MenuRating for this menu item

    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        if rating_value:
            menu_rating.ratings.create(value=rating_value, user=request.user)  # Assuming user is authenticated
            messages.success(request, 'Thank you for your rating!')

        review_text = request.POST.get('review_text')
        if review_text:
            Review.objects.create(text=review_text, menu=menu_item, user=request.user)  # Assuming user is authenticated
            messages.success(request, 'Thank you for your review!')

        return redirect('show_main', menu_id=menu_item.id)  # Redirect to avoid resubmission

    average_rating = menu_rating.average_rating()
    total_votes = menu_rating.total_votes()

    return render(request, 'ratereview.html', {
        'menu_item': menu_item,
        'average_rating': average_rating,
        'total_votes': total_votes,
        'reviews': Review.objects.filter(menu=menu_item),  # Fetch reviews for the menu item
    })