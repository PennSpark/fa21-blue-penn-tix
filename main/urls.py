from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('splash/', views.splash_view, name='splash_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('delete/', views.delete_view, name='delete_view'),
    path('like/', views.like_tweet, name='like_tweet'),
]