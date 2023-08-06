from django.urls import path,include


from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .views import (
    RegisterAPIView,
    ChangePasswordView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register_view"),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]