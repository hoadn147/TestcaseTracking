from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SignupSerializer, UserSerializer, LogOutAPISerializer, LoginSerializer , CreateTestcaseSerializer
from rest_framework.permissions import AllowAny
from .CustomRenderer import CustomRenderer

import logging


class signupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    renderer_classes = [CustomRenderer]

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
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer]

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
    renderer_classes = [CustomRenderer]

    def post(self, request):
        user = request.user
        return Response({'data': {'message': 'Logout success'}}, status=status.HTTP_200_OK)
    
class CreateTestCaseView(generics.GenericAPIView):
    serializer_class = CreateTestcaseSerializer
    renderer_classes = [CustomRenderer]
    
    def post(self, request):
        data = request.data 
        serializer = self.serializer_class()
        testcase = serializer.create(validated_data=data)
        
        return Response({'data': CreateTestcaseSerializer(testcase, context=self.get_serializer_context()).data}, status=status.HTTP_201_CREATED)
    
