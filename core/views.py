from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .serializers import SignupSerializer, UserSerializer, LogOutAPISerializer, LoginSerializer

import logging


class signupView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        logging.info('SignUp start')
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        }
        logging.info("RegisterUser success")
        return Response({"data": response_data}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, status=status.HTTP_200_OK, template_name='login.html')

    def post(self, request):
        logging.info("LoginUser start")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = str(serializer.validated_data['id'])
        username = serializer.validated_data['username']

        response = {
            'message': 'User logged in successfully',
            'id': user_id,
            'username': username,

        }
        logging.info("LoginUser success")
        return Response({'data': response}, status=status.HTTP_200_OK)


class LogOutView(generics.GenericAPIView):
    serializer_class = LogOutAPISerializer

    def post(self, request):
        user = request.user
        return Response({'data': {'message': 'Logout success'}}, status=status.HTTP_200_OK)
