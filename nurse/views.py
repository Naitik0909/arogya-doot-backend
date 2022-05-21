from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import RegisterUserSerializer
from .models import Patient
from doctor.models import Doctor, Treatment
from nurse.models import Bed, Nurse
from patient.utils import get_user
from patient.serializers import PatientSerializer
from doctor.serializers import TreatmentSerializer

class RegisterNurse(APIView):
    

    @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Same as Email'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'password2': openapi.Schema(type=openapi.TYPE_STRING, description='Confirm Password'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
        'dob': openapi.Schema(type=openapi.TYPE_STRING, description='DOB in this format: YYYY-MM-DD'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
        'blood_group': openapi.Schema(type=openapi.TYPE_STRING, description='Blood group'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age'),
        'aadhaar': openapi.Schema(type=openapi.TYPE_STRING, description='Aadhaar number'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender- Male/Female/Others'),
        'is_day_shift': openapi.Schema(type=openapi.TYPE_STRING, description='1- Day Shift | 0- Night Shift')
    }),
    responses={400: 'Bad Request'})
    def post(self, request):
        try:
            map_dict = {
                '0' : False,
                '1' : True
            }
            register = RegisterUserSerializer(data=request.data)
            if register.is_valid():
                new_user = register.save()
                if new_user:

                    nurse = Nurse.objects.create(
                        user=new_user,
                        phone=request.data.get('phone', ''),
                        address = request.data.get('address', ''),
                        dob = request.data.get('dob', ''),
                        aadhaar = request.data.get('aadhaar', ''),
                        blood_group = request.data.get('blood_group', ''),
                        age = int(request.data.get('age', '')),
                        gender = request.data.get('gender', ''),
                        is_day_shift = map_dict[request.data.get('is_day_shift', '1')]
                    )
                    
                    return JsonResponse(data={"nurse_id": nurse.id},status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(data={"error": "User not created"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"error": register.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NurseDashboard(GenericAPIView):
    
    serializer_class = PatientSerializer

    def get(self, request):
        try:
            user_id = self.request.META.get('HTTP_AUTHORIZATION')[7:]
            user = get_user(user_id)
            if not user:
                raise Exception("Invalid User")
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nurse = Nurse.objects.get(user=user)
            patients = nurse.patients.all()
            ser = self.serializer_class(patients, many=True)

            return JsonResponse(data=ser.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NurseDashboardDetail(APIView):

    def get(self, request):
        try:
            user_id = self.request.META.get('HTTP_AUTHORIZATION')[7:]
            user = get_user(user_id)
            if not user:
                raise Exception("Invalid User")
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NurseTreatmentAPI(GenericAPIView):

    serializer_class = TreatmentSerializer

    def get(self, request):
        try:
            user_id = self.request.META.get('HTTP_AUTHORIZATION')[7:]
            user = get_user(user_id)
            if not user:
                raise Exception("Invalid User")
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            patient_id = request.GET.get('patient_id', '')
            nurse = Nurse.objects.get(user=user)
            treatments = Treatment.objects.filter(nurse=nurse, patient=Patient.objects.get(id=int(patient_id)))
            ser = self.serializer_class(treatments, many=True)
            return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
