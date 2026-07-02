from django.urls import path
from .views import (
    RegisterView, LoginView, SessionLoginView, LogoutView,
    ProfileView, ChangePasswordView
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # Inscription
    path('register/', RegisterView.as_view(), name='register'),

    # Connexion JWT (RECOMMANDÉ pour React)
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Connexion Session (Alternative)
    path('session-login/', SessionLoginView.as_view(), name='session_login'),

    # Déconnexion
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profil
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
