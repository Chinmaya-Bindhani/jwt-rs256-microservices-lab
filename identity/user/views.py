from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.signals import user_logged_in
from rest_framework import generics, status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import  RefreshToken
from . serializer import  RegisterUserSerializer,LoginSerializer,ViewMe

User = get_user_model()

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh":str(refresh),
        "access": str(refresh.access_token)
    }

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username = serializer.validated_data['email'],
            password = serializer.validated_data['password']
        )
        if user is None:
            return Response(
                {"detail":"invalid email or password"},
                status= status.HTTP_401_UNAUTHORIZED,
            )
        user_logged_in.send(sender=user.__class__,request=request,user=user)

        return Response(
            {"user":ViewMe(user).data , "token":get_token(user)},
            status = status.HTTP_200_OK,
        )
    

class MeView(generics.RetrieveAPIView):
    serializer_class = ViewMe
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



