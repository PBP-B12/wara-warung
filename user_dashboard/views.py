from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import UserEntry
from .forms import EditUserProfileForm 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required(login_url='/login/')
def show_user_dashboard(request):
    user_entry, created = UserEntry.objects.get_or_create(user=request.user)

    context = {
        'username': request.user.username,
        'email': request.user.email,
        'phone_number': user_entry.phone_number if user_entry.phone_number else '',
        'address': user_entry.address if user_entry.address else '',
        'date_of_birth': user_entry.date_of_birth if user_entry.date_of_birth else '',
        'user_entry': user_entry,
    }

    return render(request, "user_dashboard.html", context)


@login_required(login_url='/login/')
def edit_user(request, id):
    user_entry = get_object_or_404(UserEntry, id=id)

    if request.method == "POST":
        form = EditUserProfileForm(request.POST, instance=user_entry)
        if form.is_valid():
            form.save()

            response_data = {
                'username': request.user.username,
                'email': request.user.email,
                'phone_number': user_entry.phone_number,
                'address': user_entry.address,
                'date_of_birth': user_entry.date_of_birth,
            }
            return JsonResponse({'status': 'success', 'data': response_data})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = EditUserProfileForm(instance=user_entry)
    context = {'form': form, 'user_entry': user_entry}
    return render(request, "edit_user.html", context)


@login_required(login_url='/login/')
def delete_account(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        user.delete()  

        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def get_user_dashboard_data(request):
    user_entry, created = UserEntry.objects.get_or_create(user=request.user)
    
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        'phone_number': user_entry.phone_number if user_entry.phone_number else '',
        'address': user_entry.address if user_entry.address else '',
        'date_of_birth': user_entry.date_of_birth if user_entry.date_of_birth else '',
    }

    return JsonResponse(user_data, status=200, safe=False)

@csrf_exempt
def update_user_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            user_entry, _ = UserEntry.objects.get_or_create(user=user)

            user.email = data.get('email', user.email)
            user.save()

            user_entry.phone_number = data.get('phone_number', user_entry.phone_number)
            user_entry.date_of_birth = data.get('date_of_birth', user_entry.date_of_birth)
            user_entry.address = data.get('address', user_entry.address)
            user_entry.save()

            return JsonResponse({"status": "success", "message": "User profile updated successfully."}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)



