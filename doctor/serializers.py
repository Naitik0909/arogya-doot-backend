from pydoc import Doc
from rest_framework import serializers

from .models import Doctor, Treatment, Observation

class DoctorSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')
    working_days = serializers.SerializerMethodField('get_working_days')

    class Meta:
        model = Doctor
        fields = '__all__'
        extra_fields = ('full_name',)

    def get_full_name(self, obj):
        return obj.user.first_name+' '+obj.user.last_name

    def get_working_days(self, obj):
        try:
            if isinstance(obj.working_days, list):
                return obj.working_days
            working_days = obj.working_days.replace('{', '')
            working_days = working_days.replace('}', '')
            # working_days[0] = '['
            # working_days[-1] = ']'
            working_days = working_days.split(",")
            working_days = [int(x) for x in working_days]
            return working_days
        except Exception as e:
            print(e)
            return ""

class TreatmentSerializer(serializers.ModelSerializer):

    nurse_name = serializers.SerializerMethodField('get_nurse_name')

    class Meta:
        model = Treatment
        fields = '__all__'
        extra_fields = ('nurse_name', )

    def get_nurse_name(self, obj):
        try:
            return obj.nurse.user.first_name+' '+obj.nurse.user.last_name
        except:
            # Nurse not assigned
            return ""

class ObservationSerializer(serializers.ModelSerializer):

    nurse_name = serializers.SerializerMethodField('get_nurse_name')

    class Meta:
        model = Observation
        fields = '__all__'
        extra_fields = ('nurse_name', )

    def get_nurse_name(self, obj):
        try:
            return obj.nurse.user.first_name+' '+obj.nurse.user.last_name
        except:
            # Nurse not assigned
            return ""