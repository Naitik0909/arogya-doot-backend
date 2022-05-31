from rest_framework import serializers

from .models import Patient
from doctor.models import Treatment, Observation

class PatientSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')
    temperature = serializers.SerializerMethodField('get_temperature')

    class Meta:
        model = Patient
        fields = '__all__'
        extra_fields = ('full_name', 'temperature')

    def get_full_name(self, obj):
        return obj.user.first_name+' '+obj.user.last_name
    
    def get_temperature(self, obj):
        try:
            # last_treatment = Treatment.objects.filter(patient=obj, treatment_type="Temperature")[0]
            last_treatment = Observation.objects.filter(patient=obj)[0]

            return last_treatment.treatment_value
        except:
            return ""
    