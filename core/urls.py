from django.urls import path, include
from .views import LoginView, LogOutView, signupView


urlpatterns = [

    path('signup', signupView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout')
]
