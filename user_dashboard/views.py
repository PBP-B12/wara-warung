from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import UserDashboard
from .forms import EditUserProfileForm  # You will need to create this form

@login_required
def show_user_dashboard(request):
    # Get the user profile information
    user_dashboard = get_object_or_404(UserDashboard, user=request.user)
    
    context = {
        'username': request.user.username,
        'email': user_dashboard.email,
        'phone_number': user_dashboard.phone_number,
        'address': user_dashboard.address,
        'date_of_birth': user_dashboard.date_of_birth,
        'budget': user_dashboard.budget,
    }

    return render(request, "user_dashboard.html", context)

@csrf_exempt
@require_POST
@login_required
def edit_user(request):
    # Get the user dashboard object for the current user
    user_dashboard = get_object_or_404(UserDashboard, user=request.user)

    if request.method == "POST" and request.is_ajax():
        form = EditUserProfileForm(request.POST, instance=user_dashboard)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
