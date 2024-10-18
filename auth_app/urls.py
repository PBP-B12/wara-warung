from django.urls import path
from auth_app.views import show_main, register, login_user, logout_user

app_name = 'auth_app'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

]