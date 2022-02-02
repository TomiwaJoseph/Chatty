from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.sign_in_or_register, name='login'),
    path('authorize/', views.login_view, name='authorize'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"), 
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), 
        name='password_reset_done'),
    path('password-reset-confim/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), 
        name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), 
        name='password_reset_complete'),
    path('awaiting-activation/', views.awaiting_activation, name='awaiting_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
