from django.urls import path
from user_dashboard.views import show_user_dashboard, edit_user, delete_account

app_name = 'user_dashboard'

urlpatterns = [
    path('', show_user_dashboard, name='show_user_dashboard'),
    path('edit-user/<int:id>', edit_user, name='edit_user'),
    path('delete/', delete_account, name='delete_user_account'),
]