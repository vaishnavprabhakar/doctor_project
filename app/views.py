from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    UserSerializer,
    BlockUsers,
    LogoutSerializer,
)
from django.db.models import Q
from .models import CustomUser
from rest_framework import views
from rest_framework.response import Response
from .tokengenerator import get_token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework import filters
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken, RefreshToken


class RegisterView(views.APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully... Login to get your token"}, status=status.HTTP_201_CREATED)
        # Registration of user and doctor is completed
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# onuulla

class LoginView(views.APIView):

    def get(self, request, format=None):

        requested_user = {
            "email": request.user.email,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }

        return Response(requested_user)

    def post(self, request, format=None):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            # print(email, password)
            user = authenticate(email=email, password=password)
            # print(user)
            if user is not None:

                tk = get_token(user)
                return Response({"msg": "login successfull", "token": tk}, status=status.HTTP_200_OK)
            return Response({"msg": "Doesn't exist. Or You must register new account"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileDetails(views.APIView):

    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):

        requested_user = {
            "email": request.user.email,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }

        return Response(requested_user)

    def patch(self, request, format=None):
        user = request.user
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Profile Updated successfully..."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        deleted_user = CustomUser.objects.filter(email=user).delete()
        return Response({"msg": "User Deleted..."})



class AdminPanel(views.APIView):

    permission_classes = [IsAdminUser]
    


    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            print(refresh_token)
            token = RefreshToken(refresh_token).blacklist()
            return Response({"msg":"You're token is blacklisted."},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get(self, request, pk=None, format=None):
        
        id = pk
        if id is not None:
            user = CustomUser.objects.get(pk = id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        user = CustomUser.objects.all()
        serializer = UserSerializer(user , many=True)
        return  Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        user = request.user
        serializer = BlockUsers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class CustomUserListView(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [filters.SearchFilter,filters.OrderingFilter]
#     search_fields = ['is_doctor','email']





class LogoutView(generics.GenericAPIView):

    serializer_class = LogoutSerializer


    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            print(refresh_token)
            token = RefreshToken(refresh_token).blacklist()
            return Response({"msg":"You're token is blacklisted."},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


