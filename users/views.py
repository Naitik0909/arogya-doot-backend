from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from .serializers import RegisterUserSerializer, BlacklistTokenSerializer

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class BlacklistToken(generics.GenericAPIView):   # For logout
    permission_classes = [AllowAny]
    serializer_class = BlacklistTokenSerializer

    def post(self, request):
        try:
            token_serializer = self.serializer_class(data=request.data)
            if token_serializer.is_valid():
                refresh_token = token_serializer.data['refresh_token']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(data={'error': token_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)