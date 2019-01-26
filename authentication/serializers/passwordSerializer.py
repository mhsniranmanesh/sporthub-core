from django.core.validators import MinLengthValidator
from rest_framework import serializers
from profiles.models import User


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['email']


class PasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[MinLengthValidator(8, 'Ensure this field has at least 8 characters.')])

    class Meta:
        model = User
        fields = ['password']
