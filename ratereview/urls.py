from django.urls import path
from ratereview.views import menu_detail,submit_review, menu_review_json, submit_review_flutter
from auth_app.views import login_view

app_name = 'ratereview'

urlpatterns = [
    path('menu/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('menu/<int:menu_id>/submit_review/', submit_review, name='submit_review'),
    path('menu/data', menu_review_json, name="menu_review_json"),
    path('menu-submit-flutter/', submit_review_flutter, name='submit_review_flutter'),
]
