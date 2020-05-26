"""ddi_development URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ddi_app.views import home, BasePageView, ProfileView, updateprofile, CreateTestPage, create_test,\
    CreateQuestionPage, create_question, TestsListView, PassTestPage, test_answer, ResultPage

urlpatterns = [
    path('', BasePageView.as_view(), name='index'),

    path('accounts/', include('allauth.urls'), name='accounts'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/<int:pk>/', updateprofile, name='updateprofile'),

    path('create_test_page/', CreateTestPage.as_view(), name='create_test_page'),
    path('create_test/<int:pk>/', create_test, name='create_test'),

    path('create_question_page/<int:pk>/', CreateQuestionPage.as_view(), name='create_question_page'),
    path('create_question/<int:pk>/', create_question, name='create_question'),

    path('tests_list_page/', TestsListView.as_view(), name='tests_list_page'),
    path('pass_test_page/<int:pk>/', PassTestPage.as_view(), name='pass_test_page'),
    path('test_answer/<int:pk>/', test_answer, name='test_answer'),
    path('result_page/<int:pk>/', ResultPage.as_view(), name='result_page'),

    path('home', home, name='home'),

    path('admin/', admin.site.urls),
]
