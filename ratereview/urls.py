from django.urls import path
from ratereview.views import menu_detail,submit_review
from auth_app.views import login_view

app_name = 'ratereview'

urlpatterns = [
    path('menu/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('menu/<int:menu_id>/submit_review/', submit_review, name='submit_review'),
]
