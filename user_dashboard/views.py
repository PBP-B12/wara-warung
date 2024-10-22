from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from user_dashboard.models import UserDashboard
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_user_dashboard(request):
    context = {
        'username': 'John Doe',
        'password': 'password',
        'email': 'email',
        'phone_number': 'phone_number',
        'address': 'address',
        'date_of_birth': 'date_of_birth',
        'budget': 'budget',
    }

    return render(request, "user_dashboard.html", context)

@csrf_exempt
@require_POST
def edit_user(request, id):
    # Get mood entry berdasarkan id
    user = UserDashboard.objects.get(pk = id)

    # Set mood entry sebagai instance dari form
    form = MoodEntryForm(request.POST or None, instance=user)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_user.html", context)