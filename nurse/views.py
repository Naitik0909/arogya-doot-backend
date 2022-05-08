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
from nurse.models import Bed, Nurse

class RegisterNurse(APIView):
    
    def post(self, request):
        try:
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
                        gender = request.data.get('gender', '')
                    )
                    
                    return JsonResponse(data={"nurse_id": nurse.id},status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(data={"error": "User not created"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data={"error": register.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)