# views.py in your warung app

from django.shortcuts import render, get_object_or_404, redirect
from .models import Warung, Menu, UserRateReview
from .forms import ReviewForm  # Assuming you have created this form

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    reviews = menu.reviews.all()  # Get all reviews related to this menu item
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.menu = menu  # Associate the review with the menu
            review.save()
            return redirect('rate_review', menu_id=menu.id)  # Redirect to the same page to see the new review

    return render(request, 'rate_review.html', {
        'menu': menu,
        'reviews': reviews,
        'form': form,
    })