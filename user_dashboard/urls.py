from django.urls import path
from user_dashboard.views import show_user_dashboard, edit_user

app_name = 'main'

urlpatterns = [
    path('', show_user_dashboard, name='show_user_dashboard'),
    path('edit-user/<uuid:id>', edit_user, name='edit_user'),
]