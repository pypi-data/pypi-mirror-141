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
    path('login/', LoginAPIView.as_view(), name="login_view"),
    path('logout/', knox_views.LogoutView.as_view(), name="logout_view"),
    path('logoutall/', LogoutAllView.as_view(), name="logout_all_view"),
    path('register/', RegisterAPIView.as_view(), name="register_view"),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
]