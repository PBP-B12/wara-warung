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

@login_required(login_url='/login')
def submit_review(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.rating = rating
            review.comment = comment
            review.menu = menu
            review.user = request.user
            review.save()

            # Calculate the new average rating
            avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
            
            # JSON response for successful submission, including the updated average rating
            return JsonResponse({
                'success': True,
                'message': "Review submitted successfully!",
                'review': {
                    'rating': review.rating,
                    'comment': review.comment,
                    'user': review.user.username,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                },
                'avg_rating': round(avg_rating, 1)  # Rounded to 1 decimal
            })
        
        # Error response for invalid form
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return redirect('ratereview:menu_detail', menu_id=menu.id)

def menu_review_json(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('json') != None:
        menu_id = request.GET.get('id', '')  # Get search query

        menu = get_object_or_404(Menu, id=menu_id)
        reviews = Review.objects.filter(menu=menu)

        data = []

        for review in reviews:
            data.append({
                'user': review.user.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at
            })

        return JsonResponse({'results': data})
