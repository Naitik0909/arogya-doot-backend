from pydoc import Doc
from rest_framework import serializers

from .models import Doctor, Treatment

class DoctorSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = Doctor
        fields = '__all__'
        extra_fields = ('full_name', )

    def get_full_name(self, obj):
        return obj.user.first_name+' '+obj.user.last_name

class TreatmentSerializer(serializers.ModelSerializer):

    nurse_name = serializers.SerializerMethodField('get_nurse_name')

    class Meta:
        model = Treatment
        fields = '__all__'
        extra_fields = ('nurse_name', )

    def get_nurse_name(self, obj):
        return obj.nurse.user.first_name+' '+obj.nurse.user.last_name