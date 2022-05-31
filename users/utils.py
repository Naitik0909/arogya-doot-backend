
from nurse.models import Nurse
from doctor.models import Doctor
from patient.models import Patient

def is_nurse(user):
    return Nurse.objects.get(user=user) if Nurse.objects.filter(user=user).exists() else False

def is_doctor(user):
    return Doctor.objects.get(user=user) if Doctor.objects.filter(user=user).exists() else False

def is_patient(user):
    return Patient.objects.get(user=user) if Patient.objects.filter(user=user).exists() else False

def is_nurse_or_doctor(user):

    # Format- [< Nurse/Doctor object >, < 0- Nurse, 1- Doctor, -1- None>]
    res = []
    if Nurse.objects.filter(user=user).exists():
        res.append(Nurse.objects.get(user=user))
        res.append(0)
    elif Doctor.objects.filter(user=user).exists():
        res.append(Doctor.objects.get(user=user))
        res.append(1)
    else:
        res.append(None)
        res.append(-1)
    return res