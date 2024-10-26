from django.urls import path, include
from . import views

app_name = 'ratereview'

urlpatterns = [
    path('', views.show_main, name='show_main'),  
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]