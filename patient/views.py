from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, pagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import RegisterUserSerializer
from .models import Patient
from doctor.models import Doctor
from nurse.models import Bed
from .utils import get_user, allocate_nurse

class RegisterPatient(APIView):
    

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
        'doctor_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Consulting Doctor id'),
        'bed_type': openapi.Schema(type=openapi.TYPE_STRING, description='Options- General/Private/Deluxe'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age'),
        'aadhaar': openapi.Schema(type=openapi.TYPE_STRING, description='Aadhaar number'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender- Male/Female/Others'),
        'emergency_contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='Emergency Contact Name'),
        'emergency_contact_phone': openapi.Schema(type=openapi.TYPE_STRING, description='Emergency Contact Phone'),
        'emergency_contact_relation': openapi.Schema(type=openapi.TYPE_STRING, description='Emergency Contact Relation'),
    }),
    responses={400: 'Bad Request'})
    def post(self, request):
        try:
            try:
                doctor = Doctor.objects.get(id=int(request.data.get('doctor_id', '')))
                bed = Bed.objects.filter(bed_type=request.data.get('bed_type', ''), is_occupied=False)[0]
            except:
                return JsonResponse(data={"error": "No beds Available for this bed type."}, status=status.HTTP_400_BAD_REQUEST)

            register = RegisterUserSerializer(data=request.data)
            if register.is_valid():
                new_user = register.save()
                if new_user:
                    
                    try:
                        print(bed)
                        patient = Patient.objects.create(
                            user=new_user,
                            phone=request.data.get('phone', ''),
                            dob=request.data.get('dob', ''),
                            address=request.data.get('address', ''),
                            blood_group=request.data.get('blood_group', ''),
                            aadhaar=request.data.get('aadhaar', ''),
                            consulting_doctor=doctor,
                            gender = request.data.get('gender', ''),
                            allocated_bed=bed,
                            # nurse allocation left to be done
                            emergency_contact_name=request.data.get('emergency_contact_name', ''),
                            emergency_contact_phone=request.data.get('emergency_contact_phone', ''),
                            emergency_contact_relation=request.data.get('emergency_contact_relation', ''),

                        )
                        if allocate_nurse(patient):
                            print("SUCCESS")
                        else:
                            print("ISSUE IN BED ALLOCATION")
                        bed.is_occupied = True
                        bed.save()
                    except IntegrityError as e:
                        print(e)
                        return Response({"error": "No Bed Available"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    return JsonResponse(data={"patient_id": patient.id},status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(data={"error": "User not created"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"error": register.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NursePatientDetails(APIView):

    def get(self, request):
        try:
            token = request.data.get("access", "")
            user = get_user(token)
        except Exception as e:
            return JsonResponse(data={"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        