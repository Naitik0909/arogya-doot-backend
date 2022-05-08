from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from patient.models import Patient
from doctor.models import Doctor
from nurse.models import Nurse

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )


        user.set_password(validated_data['password'])
        user.save()

        return user

class BlacklistTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)

    def validate(self, attrs):
        if len(attrs['refresh_token']) < 10:
            raise serializers.ValidationError({"refresh_token": 'Token too short'})

        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        user_type = None
        user = self.user
        if Patient.objects.filter(user = user).exists():
            user_type = 'Patient'
        elif Nurse.objects.filter(user=user).exists():
            user_type = 'Nurse'
        elif Doctor.objects.filter(user=user).exists():
            user_type = 'Doctor'
        data['user'] = user_type
        return data
    default_error_messages = {
        'no_active_account': _('Please enter correct credentials.')
    }