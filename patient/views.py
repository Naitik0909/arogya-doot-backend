from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics, pagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from doctor.serializers import ObservationSerializer, TreatmentSerializer

from users.serializers import RegisterUserSerializer
from .serializers import PatientSerializer
from nurse.serializers import ReportSerializer
from .models import Patient
from doctor.models import Doctor, Observation, Treatment
from nurse.models import Bed, Nurse, Report
from .utils import get_user, allocate_nurse
from users.utils import is_nurse_or_doctor
from .mail_handler import send_email_to_user

from datetime import datetime

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

class CurrentPatientDetails(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PatientSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            serializer = self.serializer_class(patient)
            return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailsAPI(GenericAPIView):
    
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        res = is_nurse_or_doctor(user)

        try:
            if res[0] == None:
                return JsonResponse(data={"error": "Unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                patient_id = kwargs["pk"]
                patient = Patient.objects.get(id=int(patient_id))

                if res[1] == 0:
                    # Its a nurse
                    nurse = res[0]
                    if(patient in nurse.patients.all()):
                        ser = PatientSerializer(patient)
                        return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(data={"error": "This doctor is currently not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)


                elif res[1] == 1:
                    # Its a doctor
                    doctor = res[0]
                    if(doctor == patient.consulting_doctor):
                        ser = PatientSerializer(patient)
                        return JsonResponse(data=ser.data, safe=False,status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(data={"error": "This doctor is currently not treating this patient"}, status=status.HTTP_401_UNAUTHORIZED)


        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class PatientListAPI(GenericAPIView):
    
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        res = is_nurse_or_doctor(user)

        try:
            if res[0] == None:
                return JsonResponse(data={"error": "Unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if res[1] == 0:
                    # Its a nurse
                    nurse = res[0]
                    patients = nurse.patients.all()
                    ser = self.serializer_class(patients, many=True)

                    return JsonResponse(data=ser.data, safe=False, status=status.HTTP_200_OK)


                elif res[1] == 1:
                    # Its a doctor
                    doctor = res[0]
                    patients = Patient.objects.filter(consulting_doctor=doctor)
                    ser = self.serializer_class(patients, many=True)
                    return JsonResponse(data=ser.data, safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PatientObservationsAPI(GenericAPIView):

    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            observations = Observation.objects.filter(patient=patient)
            ser = self.serializer_class(observations, many=True)
            return JsonResponse(data=ser.data, safe=False, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return JsonResponse(data={"error": "Patient does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PatientTreatmentsAPI(GenericAPIView):

    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            treatments = Treatment.objects.filter(patient=patient)
            ser = self.serializer_class(treatments, many=True)
            return JsonResponse(data=ser.data, safe=False, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return JsonResponse(data={"error": "Patient does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LandingPageAPI(APIView):

    def get(self, request):
        try:
            data = {
                "total_beds" : Bed.objects.all().count(),
                "total_patients" : Patient.objects.all().count(),
                "total_doctors" : Doctor.objects.all().count(),
                "total_nurses" : Nurse.objects.all().count(),
            }
            return JsonResponse(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LandingPagePieAPI(APIView):

    def get(self, request):
        try:
            data={}
            bed_type = ["General", "Private", "Deluxe"]

            for bed in bed_type:
                data[bed] = {
                    "total": Bed.objects.filter(bed_type=bed).count(),
                    "occupied": Bed.objects.filter(bed_type=bed, is_occupied=True).count()
                }

            
            return JsonResponse(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LandingPageGraphAPI(APIView):

    def get(self, request):
        try:
            data={}

            for pat in Patient.objects.all():
                month = datetime.strftime(pat.created_at, '%B')
                if month in data:
                    data[month] += 1
                else:
                    data[month] = 1
            
            return JsonResponse(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReportAPI(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer

    def get(self, request):
        try:
            patient = Patient.objects.get(id=int(request.GET.get("patient_id")))
            reports = Report.objects.filter(patient=patient)
            ser = self.serializer_class(reports, many=True)
            return JsonResponse(data=ser.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            # user = request.user
            patient = Patient.objects.get(id=int(request.POST["patient_id"]))
            report = request.FILES.get('report_file')
            report_obj = Report.objects.create(
                patient = patient,
                report_name = request.POST.get('report_name', ''),
                report_file = report,
                uploaded_by = f"{request.user.first_name} {request.user.last_name}"
            )

            return JsonResponse(data={"status": "success"}, status=status.HTTP_201_CREATED)
            
        except Patient.DoesNotExist:
            return JsonResponse(data={"error": "Patient does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TempGraphAPI(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            data = {}

            observations = Observation.objects.filter(patient=patient)

            for obs in observations:
                if obs.created_at.strftime("%-d %b") in data:
                    data[obs.created_at.strftime("%-d %b")].append(obs.temperature)
                else:
                    data[obs.created_at.strftime("%-d %b")] = [obs.temperature]

            return JsonResponse(data=data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SOSMailAPI(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            patient_id = request.GET.get("patient_id")
            patient = Patient.objects.get(id=int(patient_id))
            send_email_to_user("parmarnaitik0909@gmail.com", patient)
            return JsonResponse(data={"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)