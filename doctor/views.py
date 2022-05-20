from pydoc import doc
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import RegisterUserSerializer
from .serializers import DoctorSerializer, TreatmentSerializer
from .models import Patient
from doctor.models import Doctor, Treatment
from nurse.models import Bed, Nurse
from patient.utils import get_user

class RegisterDoctor(APIView):
    
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
        'specialization': openapi.Schema(type=openapi.TYPE_STRING, description='Specialization'),
    }),
    responses={400: 'Bad Request'})
    def post(self, request):
        try:
            register = RegisterUserSerializer(data=request.data)
            if register.is_valid():
                new_user = register.save()
                if new_user:

                    doctor = Doctor.objects.create(
                        user=new_user,
                        phone=request.data.get('phone', ''),
                        address = request.data.get('address', ''),
                        dob = request.data.get('dob', ''),
                        aadhaar = request.data.get('aadhaar', ''),
                        blood_group = request.data.get('blood_group', ''),
                        age = int(request.data.get('age', '')),
                        gender = request.data.get('gender', ''),
                        location = request.data.get('location', ''),
                        specialization = request.data.get('specialization', '')
                    )
                    
                    return JsonResponse(data={"doctor_id": doctor.id},status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(data={"error": "User not created"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"error": register.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompleteTreatment(APIView):

    def post(self, request):

        try:
            user = request.data.get('access', '')
            get_user(user)

            patient_id = request.data.get('patient_id', '')
            if patient_id != '':
                patient = Patient.objects.get(id=patient_id)
                doctor = Doctor.objects.get(user=user)

                if patient.consulting_doctor == doctor:
                    # find out the nurse with max number of patients
                    all_nurses = Nurse.objects.all()
                    max = 0
                    max_nurse = None
                    for nurse in all_nurses:
                        count = nurse.patients.all().count()
                        if count > max:
                            max = count
                            max_nurse = nurse

                    # current_nurse = Nurse.objects.get(patients__in=)

        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DoctorDetail(GenericAPIView):

    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('access', '')
            user = get_user(user_id)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        doc_id = int(kwargs["pk"])
        ser = self.serializer_class(Doctor.objects.get(id=doc_id))
        return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)

        
class DoctorTreatmentAPI(GenericAPIView):

    serializer_class = TreatmentSerializer

    def get(self, request):
        try:
            user_id = request.data.get('access', '')
            user = get_user(user_id)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        doctor = Doctor.objects.get(user=user)
        treatments = Treatment.objects.filter(doctor=doctor)
        ser = self.serializer_class(treatments, many=True)
        return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user_id = request.data.get('access', '')
            user = get_user(user_id)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
