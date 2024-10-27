from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from auth_app.forms import UserRegisterForm
from auth_app.models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



def main_view(request):
    return render(request, 'homepage.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun untuk {username} berhasil dibuat!')
            return redirect('auth_app:login')  # Ubah dengan URL login Anda
        else:
            # Jika form tidak valid, pesan kesalahan akan ditampilkan di template
            messages.error(request, 'Pendaftaran gagal. Silakan periksa kesalahan di bawah ini.')
    else:
        form = UserCreationForm()

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
                return redirect('auth_app:main')  # Redirect to the main page after login
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid login details. Please check your username and password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('auth_app:main')  # Gunakan namespace jika ada

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm

def main_view(request):
    return render(request, 'main.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Buat profil jika belum ada
            Profile.objects.get_or_create(user=user)
            
            # Login pengguna setelah registrasi berhasil
            login(request, user)
            return redirect('auth_app:login')  # Gunakan namespace jika ada
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
                return redirect('auth_app:main')  # Arahkan ke halaman utama setelah login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('auth_app:main')  # Gunakan namespace jika ada

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})
