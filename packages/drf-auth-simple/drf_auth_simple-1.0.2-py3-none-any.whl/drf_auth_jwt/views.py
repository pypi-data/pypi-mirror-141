from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,UpdateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView


from django.contrib.auth import get_user_model,login,logout


from .serializers import UserSerializer,RegisterSerializer,ChangePasswordSerializer,RefreshTokenSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

UserModel = get_user_model()

from rest_framework_simplejwt.authentication import JWTAuthentication



class BlacklistTokenUpdateView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class LogoutAllView(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        outstandingTokens = OutstandingToken.objects.filter(user=user)

        if outstandingTokens:
            for outstandingToken in outstandingTokens:
                token_base_encoded_string = outstandingToken.token
                try :
                    token = RefreshToken(token_base_encoded_string)
                    token.blacklist()
                except :
                    pass
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

class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user



class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user

###########################################################
#                   PASSWORD RESET                        #
###########################################################

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

from .utils import Util


class RequestPasswordResetEmailView(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def create_link(self,user,request):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        #current_site = FRONTEND URL
        
        current_site = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        absurl = 'http://' + current_site + relativeLink

        return absurl
    
    def create_emaildata(self,user,absurl):
        email_body = 'Hello, \n Use link below to reset your password  \n'+absurl
            
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Reset your passsword'
        }
        return data

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if UserModel.objects.filter(email=email).exists():
            user = UserModel.objects.get(email=email)
            
            link = self.create_link(user=user,request=request)
            data = self.create_emaildata(user=user,absurl=link)
            
            Util.send_email(data)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'E-mail does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            
            success = {
                'success' : True,
                'message' : 'Credentials Valid',
                'uidb64'  : uidb64,
                'token'   : token 
            }
            return Response(success, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)