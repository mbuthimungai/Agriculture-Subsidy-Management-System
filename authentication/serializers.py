from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'username')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True}
        }

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'password',)
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}            
        }