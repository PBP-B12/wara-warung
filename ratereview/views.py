from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from menu.models import Menu  # Import Menu from the menu app
from django.db.models import Avg
from .models import Review
from .forms import ReviewForm
from django.http import JsonResponse

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    reviews = Review.objects.filter(menu=menu)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    form = ReviewForm()  # Pass an empty form for new submissions

    return render(request, 'menu_detail.html', {
        'menu': menu,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form
    })


@login_required
def submit_review(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.rating = rating
        review.comment = comment
        review.menu = menu
        review.user = request.user
        review.save()
        
        # JSON response for successful submission
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': "Review submitted successfully!",
                'review': {
                    'rating': review.rating,
                    'comment': review.comment,
                    'user': review.user.username,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        
        # Regular redirect if not an AJAX request
        return redirect('ratereview:menu_detail', menu_id=menu.id)

    return redirect('ratereview:menu_detail', menu_id=menu.id)