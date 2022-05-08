from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, pagination

from users.serializers import RegisterUserSerializer
from .models import Patient
from doctor.models import Doctor
from nurse.models import Bed

class RegisterPatient(APIView):
    
    def post(self, request):
        try:
            register = RegisterUserSerializer(data=request.data)
            if register.is_valid():
                new_user = register.save()
                if new_user:
                    doctor = Doctor.objects.get(id=int(request.data.get('doctor_id', '')))
                    bed = Bed.objects.filter(bed_type=request.data.get('bed_type', ''))[0]
                    try:
                        patient = Patient.objects.create(
                            user=new_user,
                            phone=request.data.get('phone', ''),
                            dob=request.data.get('dob', ''),
                            address=request.data.get('address', ''),
                            blood_group=request.data.get('blood_group', ''),
                            aadhaar=request.data.get('aadhaar', ''),
                            consulting_doctor=doctor,
                            allocated_bed=bed,
                            # nurse allocation left to be done
                            emergency_contact_name=request.data.get('emergency_contact_name', ''),
                            emergency_contact_phone=request.data.get('emergency_contact_phone', ''),
                            emergency_contact_relation=request.data.get('emergency_contact_relation', ''),

                        )
                    except IntegrityError as e:
                        return Response({"message": "No Bed Available"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    return JsonResponse(data={"patient_id": patient.id},status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(data={"error": "User not created"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"error": register.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)