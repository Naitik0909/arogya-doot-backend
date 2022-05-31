from pydoc import doc
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import RegisterUserSerializer
from .serializers import DoctorSerializer, TreatmentSerializer, ObservationSerializer
from .models import Patient
from doctor.models import Doctor, Treatment, Observation
from nurse.models import Bed, Nurse
from patient.utils import get_user

class RegisterDoctor(APIView):

    permission_classes = [AllowAny]
    
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
                        specialization = request.data.get('specialization', ''),
                        working_days = list(request.data.get('working_days', '')),
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
            user_id = self.request.META.get('HTTP_AUTHORIZATION')[7:]
            user = get_user(user_id)
            if not user:
                raise Exception("Invalid User")

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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # try:
        #     user_id = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        #     user = get_user(user_id)
        #     if not user:
        #         raise Exception("Invalid User")
        # except Exception as e:
        #     return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # print(self.request.user)
        doc_id = int(kwargs["pk"])
        ser = self.serializer_class(Doctor.objects.get(id=doc_id))
        return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)

        
class DoctorTreatmentAPI(GenericAPIView):

    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            patient_id = request.GET.get('patient_id', '')
            doctor = Doctor.objects.get(user=user)
            patient = Patient.objects.get(id=int(patient_id))

            # Check if that Doctor is treating that patient:
            if patient.consulting_doctor == doctor:
                treatments = Treatment.objects.filter(patient=patient)
                ser = self.serializer_class(treatments, many=True)
                return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)
            else:
                return JsonResponse(data={"error": "You are not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        user = request.user
        
        try:
            patient_id = request.data.get('patient_id', '')
            doctor = Doctor.objects.get(user=user)
            patient = Patient.objects.get(id=int(patient_id))

            # Check if that Doctor is treating that patient:
            if patient.consulting_doctor == doctor:
                treatment = Treatment.objects.create(
                    patient=patient,
                    treatment = request.data.get('treatment', ''),
                    details=request.data.get('details', ''),
                    treatment_time=request.data.get('treatment_time', '')
                )
                return JsonResponse(data={"treatment_id": treatment.id}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(data={"error": "You are not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        user = request.user
        try:
            treatment_id = request.data.get('treatment_id', '')
            doctor = Doctor.objects.get(user=user)
            treatment = Treatment.objects.get(id=int(treatment_id))

            # Check if that Doctor is treating that patient:
            if treatment.patient.consulting_doctor == doctor:
                treatment.treatment = request.data.get('treatment', '')
                treatment.details = request.data.get('details', '')
                treatment.treatment_time = request.data.get('treatment_time', None)
                treatment.save()
                return JsonResponse(data={"success": "Treatment updated"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(data={"error": "You are not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class DoctorObservation(GenericAPIView):

    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            patient_id = request.GET.get('patient_id', '')
            doctor = Doctor.objects.get(user=user)
            patient = Patient.objects.get(id=int(patient_id))

            # Check if that Doctor is treating that patient:
            if patient.consulting_doctor == doctor:
                observations = Observation.objects.filter(patient=patient)
                ser = self.serializer_class(observations, many=True)
                return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)
            else:
                return JsonResponse(data={"error": "You are not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        user = request.user

        try:
            patient_id = request.data.get('patient_id', '')
            doctor = Doctor.objects.get(user=user)
            patient = Patient.objects.get(id=int(patient_id))
            # Check if that Doctor is treating that patient:
            if patient.consulting_doctor == doctor:
                observations = Observation.objects.create(
                    patient=patient,
                    temperature = request.data.get('temperature', ''),
                    blood_pressure = request.data.get('blood_pressure', ''),
                    oxygen_level = request.data.get('oxygen_level', ''),
                    heart_rate = request.data.get('heart_rate', ''),
                    comment = request.data.get('comment', '')
                )
                return JsonResponse(data={"observation_id": observations.id}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(data={"error": "You are not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TopDoctorsAPI(APIView):

    def get(self, request):
        doc_list = {}
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()

        for pat in patients:
            if pat.consulting_doctor.id not in doc_list:
                doc_list[pat.consulting_doctor.id] = 1
            else:
                doc_list[pat.consulting_doctor.id] += 1
        doc_list = {k: v for k, v in sorted(doc_list.items(), key=lambda item: item[1])}

        return JsonResponse(data=doc_list, safe=False,status=status.HTTP_200_OK)