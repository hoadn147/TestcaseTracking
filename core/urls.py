from django.urls import path
from .views import signup, index 

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
]
