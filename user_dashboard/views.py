from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import UserEntry
from .forms import EditUserProfileForm 

@login_required
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


@login_required
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


@login_required
def delete_account(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        user.delete()  

        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})




