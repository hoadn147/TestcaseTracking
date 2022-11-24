from rest_framework import serializers
from.models import *
from rest_framework.exceptions import AuthenticationFailed, APIException, NotFound
import logging
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password',)
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    def create(self, validated_data):
        try:
            user = User()
            user.set_password(validated_data.get("password"))
            user.username = validated_data['username']
            user.save()
            
        except Exception as e:
           logging.error("User already exists!")
           raise APIException("User already exists!") from e
        return user
    
class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username')
        
    def validate(self, attrs):
        user_id = attrs.get('id')
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            logging.error(f"UserSerializer error: {e}")
            raise APIException("User doesn't exist") from e
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('password',)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Email and password are invalid, try again!')

        return {
            'id': user.id,
            'username': user.get_username
        }
        
        
class LogOutAPISerializer(serializers.Serializer):

    def validate(self, attrs):
        return attrs   