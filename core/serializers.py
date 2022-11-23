from rest_framework import serializers
from.models import *

class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        