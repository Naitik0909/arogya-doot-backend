import re
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
from doctor.models import Doctor
from nurse.models import Nurse
from patient.models import Patient

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

    def put(self, request):
        user = request.user

        try:
            role = request.data.get('role')
            str_to_bool = {
                "0": True,
                "1": False
            }

            if role == "Patient":
                patient = Patient.objects.get(user=user)
                patient.user.first_name = request.data.get('first_name', '')
                patient.user.last_name = request.data.get('last_name', '')
                patient.phone = request.data.get('phone', '')
                patient.address = request.data.get('address', '')
                patient.age = request.data.get('age', '')
                patient.dob = request.data.get('dob', '')
                patient.gender = request.data.get('gender', '')
                patient.blood_group = request.data.get('blood_group', '')
                patient.aadhaar = request.data.get('aadhaar', '')
                patient.emergeny_contact_name = request.data.get('emergeny_contact_name', '')
                patient.emergeny_contact_phone = request.data.get('emergeny_contact_phone', '')
                patient.emergency_contact_relation = request.data.get('emergency_contact_relation', '')
                patient.save()
            
            elif role == "Doctor":
                doctor = Doctor.objects.get(user=user)
                doctor.user.first_name = request.data.get('first_name', '')
                doctor.user.last_name = request.data.get('last_name', '')
                doctor.phone = request.data.get('phone', '')
                doctor.address = request.data.get('address', '')
                doctor.age = request.data.get('age', '')
                doctor.dob = request.data.get('dob', '')
                doctor.gender = request.data.get('gender', '')
                doctor.blood_group = request.data.get('blood_group', '')
                doctor.aadhaar = request.data.get('aadhaar', '')
                doctor.working_days = list(request.data.get('working_days', ''))
                doctor.specialization = request.data.get('specialization', '')
                doctor.location = request.data.get('location', '')
                doctor.save()
            
            elif role == "Nurse":
                nurse = Nurse.objects.get(user=user)
                nurse.user.first_name = request.data.get('first_name', '')
                nurse.user.last_name = request.data.get('last_name', '')
                nurse.phone = request.data.get('phone', '')
                nurse.address = request.data.get('address', '')
                nurse.age = request.data.get('age', '')
                nurse.dob = request.data.get('dob', '')
                nurse.gender = request.data.get('gender', '')
                nurse.blood_group = request.data.get('blood_group', '')
                nurse.aadhaar = request.data.get('aadhaar', '')
                # nurse.is_day_shift = request.data.get('is_day_shift', '')
                nurse.save()
            return JsonResponse(data={"success": "Updated Data"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)