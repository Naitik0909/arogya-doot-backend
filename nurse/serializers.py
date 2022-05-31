from rest_framework import serializers

from .models import Nurse

class NurseSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = Nurse
        fields = '__all__'
        extra_fields = ('full_name', )

    def get_full_name(self, obj):
        return obj.user.first_name+' '+obj.user.last_name
