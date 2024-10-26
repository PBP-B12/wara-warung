from django.urls import path
from ratereview.views import menu_item_detail

app_name = 'main'

urlpatterns = [
    path('ratereview/<int:menu_item_id>/', menu_item_detail, name='menu_item_detail'),
]
