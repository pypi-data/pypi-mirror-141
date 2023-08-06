from django.urls import path,include


from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .views import (
    LoginAPIView,
    LogoutAllView,
    RegisterAPIView,
    ChangePasswordView,
)

from knox import views as knox_views

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name="login_view"),
    path('auth/logout/', knox_views.LogoutView.as_view(), name="logout_view"),
    path('auth/logoutall/', LogoutAllView.as_view(), name="logout_all_view"),
    path('auth/register/', RegisterAPIView.as_view(), name="register_view"),
    path('auth/change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
]