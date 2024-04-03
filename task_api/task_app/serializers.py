from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields ="__all__"


class UserSerializer(serializers.ModelSerializer):
    developer = TaskSerializer(read_only=True, many=True)
    password = serializers.CharField(write_only=True , style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    is_active = serializers.BooleanField(read_only=True)
    last_login = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields ="__all__"
    
    def validate(self, attr):
        password = attr.get("password")
        password2 = attr.get("password2")

        if password != password2:
            raise ValidationError("password and confirm_password dosent match")
        return attr
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)

    class Meta:
        model = User
        fields = ['email', 'password']


