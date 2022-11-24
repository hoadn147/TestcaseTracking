from django.urls import path, include
from .views import LoginView, LogOutView, signupView, CreateTestCaseView


urlpatterns = [

    path('signup', signupView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('testcase-create', CreateTestCaseView.as_view(), name='testcase-create')
]
