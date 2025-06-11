from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-confirm/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]