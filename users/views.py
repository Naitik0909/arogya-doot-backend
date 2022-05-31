from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

import nurse


from .serializers import RegisterUserSerializer, BlacklistTokenSerializer, CustomTokenObtainPairSerializer
from .utils import is_doctor, is_nurse, is_patient
from doctor.serializers import DoctorSerializer
from patient.serializers import PatientSerializer
from nurse.serializers import NurseSerializer

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

class LoginUser(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GetUserDetails(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            ser = None
            doctor = is_doctor(user)
            role = ""
            if doctor:
                ser = DoctorSerializer(doctor)
                role = "Doctor"
            nurse = is_nurse(user)
            if nurse:
                ser = NurseSerializer(nurse)
                role = "Nurse"
            patient = is_patient(user)
            if patient:
                ser = PatientSerializer(patient)
                role = "Patient"
            final_data = {
                "details": ser.data,
                "role": role
            }

            return JsonResponse(final_data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

