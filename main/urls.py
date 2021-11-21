from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.main_view, name="main_view"),
    path("tickets/", views.tickets_view, name="tickets_view"),
    path("sell/", views.sell_view, name="sell_view"),
    path("profile/", views.profile_view, name="profile_view"),
    
    path("splash/", views.splash_view, name="splash_view"),
    path("login/", views.login_view, name="login_view"),
    path("signup/", views.signup_view, name="signup_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("delete/", views.delete_view, name="delete_view"),
]
