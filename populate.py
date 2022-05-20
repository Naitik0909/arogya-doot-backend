import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','arogya_doot_backend.settings')

# Setting up django configurations
import django
django.setup()

import random
from nurse.models import Bed


def populate_beds():
    count = 2
    BED_TYPE = ['General', 'Private', 'Deluxe']

    for i in range(15):
        Bed.objects.create(
            bed_type= random.choice(BED_TYPE),
            number = count
        )
        count+=1

populate_beds()
