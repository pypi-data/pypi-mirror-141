from django.urls import path,include


from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .views import (
    RegisterAPIView,
    ChangePasswordView,
    BlacklistTokenUpdateView,
    LogoutAllView,
    UserAPIView,
    UserUpdateAPIView,
    RequestPasswordResetEmailView,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register_view"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', BlacklistTokenUpdateView.as_view(), name='auth_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='auth_logout_all_relational_user'),


    path('user/', UserAPIView.as_view(), name='user_detail'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('user/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('request-password-reset-email/', RequestPasswordResetEmailView.as_view(), name="request-reset-email"),
    path('check-password-reset/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('complete-password-reset/',SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

]