from sqlite3 import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import FilterRequirementSerializer, SignupSerializer, UserSerializer, LogOutAPISerializer, LoginSerializer , CreateTestcaseSerializer
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
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            testcase = serializer.create(validated_data=serializer.validated_data)
        except IntegrityError or ValueError as e:
            return Response({'data': None, 'exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': CreateTestcaseSerializer(testcase, context=self.get_serializer_context()).data}, status=status.HTTP_201_CREATED)


class FilterRequirementView(generics.GenericAPIView):
    serializer_class = FilterRequirementSerializer
    renderer_classes = [CustomRenderer]
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.validated_data}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        data = request.GET
        serializer = self.serializer_class(data=data)
        print('2222222222222222222222222', serializer)
        serializer.is_valid(raise_exception=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request):
        ...
    
