from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .models import User, subTab, requirementFilter


class signupViewset(generics.GenericAPIView):
    
    serializer_class = 
