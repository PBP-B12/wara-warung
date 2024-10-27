from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from auth_app.forms import UserRegisterForm
from auth_app.models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def main_view(request):
    return render(request, 'homepage.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun untuk {username} berhasil dibuat!')
            return redirect('auth_app:login')
        else:
            messages.error(request, 'Pendaftaran gagal. Silakan periksa kesalahan di bawah ini.')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('auth_app:main')
            else:
                messages.error(request, 'Invalid username or password. Please try again.', extra_tags="auth")
        else:
            messages.error(request, 'Invalid login details. Please check your username and password.', extra_tags="auth")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('auth_app:main')
