from django.urls import path, include
from .views import *


urlpatterns = [

    path('signup', SignupView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('testcase', CreateTestCaseView.as_view(), name='testcase'),
    path('filter-requirement', FilterRequirementView.as_view(), name='filter-requirement'),
    path('filter-requirement-update', FilterRequirementUpdateView.as_view(), name= 'filter-requirement-update'),
    path('test-case-update', TestcaseUpdateView.as_view(), name= 'test-case-update'),
    path('sub-tab-search', SubTabSearchView.as_view(), name= 'sub-tab-search'),
    path('filter-search', GetAllFilterView.as_view(), name= 'filter-search'),
]
