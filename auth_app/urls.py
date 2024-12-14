from django.urls import path
from . import views

app_name = 'auth_app'  # Inisialisasi namespace

urlpatterns = [
    path('', views.main_view, name='main'),  # Tambahkan halaman utama
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('auth/registerd/', views.register, name='registerd'),
    path('auth/logind/', views.login, name='logind'),
    path('auth/logoutd/', views.logout, name='logout'),
    ]
