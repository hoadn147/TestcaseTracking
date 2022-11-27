from django.urls import path, include
from .views import FilterRequirementView, LoginView, LogOutView, signupView, CreateTestCaseView, FilterRequirementUpdateView


urlpatterns = [

    path('signup', signupView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('testcase', CreateTestCaseView.as_view(), name='testcase'),
    path('filter-requirement', FilterRequirementView.as_view(), name='filter-requirement'),
    path('filter-requirement-update', FilterRequirementUpdateView.as_view(), name= 'filter-requirement-update')
]
