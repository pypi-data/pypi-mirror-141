from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from knox.models import AuthToken
from knox.auth import TokenAuthentication


from django.contrib.auth import get_user_model,login,logout


from .serializers import LoginSerializer,UserSerializer,RegisterSerializer,ChangePasswordSerializer



UserModel = get_user_model()

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email', None)

        user = UserModel.objects.get(email=email)

        instance, token = AuthToken.objects.create(user)
        login(request, user)
        return Response({
            "user"  : UserSerializer(user,context=serializer).data,
            "token" : token
        })



class LogoutAllView(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (TokenAuthentication,SessionAuthentication)
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

        instance, token = AuthToken.objects.create(user)
        login(request, user)
        return Response({
            "user"  : UserSerializer(user,context=serializer).data,
            "token" : token
        })
    
class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=UserModel):
        return self.request.user
