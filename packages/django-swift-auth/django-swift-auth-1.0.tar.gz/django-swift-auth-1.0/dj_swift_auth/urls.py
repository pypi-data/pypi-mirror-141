from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/', CreateUserView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/change-password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
]
