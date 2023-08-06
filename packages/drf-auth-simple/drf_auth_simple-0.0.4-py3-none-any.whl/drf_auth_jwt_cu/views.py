from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView



from django.contrib.auth import get_user_model,login,logout


from .serializers import UserSerializer,RegisterSerializer,ChangePasswordSerializer


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

UserModel = get_user_model()

from rest_framework_simplejwt.authentication import JWTAuthentication


class LogoutAllView(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (JWTAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)



    
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request, user)
        return Response({
            "user"  : UserSerializer(user,context=serializer).data,
            "token" : get_tokens_for_user(user)
        })
    
class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=UserModel):
        return self.request.user
