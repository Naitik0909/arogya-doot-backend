
from nurse.models import Nurse

def is_nurse(user):
    return Nurse.objects.get(user=user) if Nurse.objects.filter(user=user).exists() else False
