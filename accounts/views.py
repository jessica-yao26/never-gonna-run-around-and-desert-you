from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer, TokenCreateSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken

User = get_user_model()


class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserExistsByEmail(APIView):

    def get(self, request, *args, **kwargs):
        # use this if username is in url kwargs
        #username = self.kwargs.get('username') 

        # use this if username is being sent as a query parameter
        email = self.request.query_params.get('email')  

        try:
            user = User.objects.get(email=email) # retrieve the user using username
            users = User.objects.all()
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # return false as user does not exist
        else:
            return Response(status=status.HTTP_200_OK) # Otherwise, return True

class UserExistsByUsername(APIView):

    def get(self, request, *args, **kwargs):
        # use this if username is in url kwargs
        #username = self.kwargs.get('username') 

        # use this if username is being sent as a query parameter
        username = self.request.query_params.get('username')  
        try:
            user = User.objects.get(username=username) # retrieve the user using username
            users = User.objects.all()
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # return false as user does not exist
        else:
            return Response(status=status.HTTP_200_OK) # Otherwise, return True

class UserExistsByUsername(APIView):

    def get(self, request, *args, **kwargs):
        # use this if username is in url kwargs
        #username = self.kwargs.get('username') 

        # use this if username is being sent as a query parameter
        username = self.request.query_params.get('username')  
        try:
            user = User.objects.get(username=username) # retrieve the user using username
            users = User.objects.all()
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # return false as user does not exist
        else:
            return Response(status=status.HTTP_200_OK) # Otherwise, return True

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = TokenCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
