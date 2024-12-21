import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from menu.models import Menu  # Import Menu from the menu app
from django.db.models import Avg
from .models import Review
from .forms import ReviewForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def menu_data_flutter(request):
    if request.method == 'POST':
        data_req = json.loads(request.body)
        username = request.user.username
        query = data_req['query']
        budget = data_req['budget']
        warung = data_req['warung']
        results = Menu.objects.all()
        if query:
            results = results.filter(menu__icontains=query)

        if budget:
            results = results.filter(harga__lte=int(budget))
        
        if warung:
            results = results.filter(warung__icontains=warung)
        
        data = []
        for menu in results:
            avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
            data.append({
                'menu': menu.menu,
                'harga': menu.harga,
                'warung': menu.warung,
                'gambar': menu.gambar,
                'id': menu.id,
                'avg_rating': round(avg_rating, 1)  # One decimal place
            })
        response = JsonResponse({'results': data, 'username': username})
        return response

@csrf_exempt 
def menu_review_json(request):
    if request.method == 'POST':
        data_req = json.loads(request.body)
        menu_id = data_req['id']

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
    
@csrf_exempt
def submit_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu = get_object_or_404(Menu, id=int(data['id']))
        new_review = Review.objects.create(
            menu=menu,
            user=request.user,
            rating=int(data['rating']),
            comment=data['comment'],
        )
        new_review.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def avg_rate_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu = get_object_or_404(Menu, id=int(data['id']))
        reviews = Review.objects.filter(menu=menu)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        return JsonResponse({'avg_rating': round(avg_rating, 1)})

