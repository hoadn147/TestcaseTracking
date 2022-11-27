from sqlite3 import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from core.models import User, requirementFilter, subTab
from .serializers import *
from rest_framework.permissions import AllowAny
from .CustomRenderer import CustomRenderer
from django.db import transaction
import logging
import json


class signupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    renderer_classes = [CustomRenderer]

    def post(self, request):
        logging.info('SignUp start')
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            User.create_relative_parent_tab(user)
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

    def get(self, request):
        data = request.GET
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')
        req_id = data.get('req_id')
        testcase_id = data.get('testcase_id')

        try:
            if not user_id or not parent_tab_name:
                return Response({'exception': 'user_id and parent_tab_name are required for receiving single filter'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                testcase = subTab.objects.filter(
                    req_id=req_id,
                    parent_tab__user_id=user_id,
                    parent_tab__tab_name=parent_tab_name,
                    testcase_id=testcase_id,
                )
            serializer = self.serializer_class(testcase, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            testcase = serializer.create(
                validated_data=serializer.validated_data)
        except IntegrityError or ValueError as e:
            return Response({'data': None, 'exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': CreateTestcaseSerializer(testcase, context=self.get_serializer_context()).data}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        testcase_id = request.data.get('id')
        try:
            testcase = subTab.objects.get(pk=testcase_id)
            testcase.delete()
        except testcase.DoesNotExist:
            raise APIException("Testcase does not exist")
        return Response({'data': {'message': 'Delete success'}}, status=status.HTTP_200_OK)


class FilterRequirementView(generics.GenericAPIView):
    serializer_class = FilterRequirementSerializer
    renderer_classes = [CustomRenderer]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            filter = serializer.save()
        except Exception as e:
            return Response({'data': None, 'exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': filter}, status=status.HTTP_201_CREATED)

    def get(self, request):
        data = request.GET
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')

        if not user_id or not parent_tab_name:
            return Response({'exception': 'user_id and parent_tab_name are required for receiving single filter'}, status=status.HTTP_400_BAD_REQUEST)
        if data.get('req_id') and data.get('filter_name'):
            filter_requirement = requirementFilter.objects.filter(
                req_id=data.get('req_id'),
                parent_tab__user_id=data.get('user_id'),
                parent_tab__tab_name=data.get('parent_tab_name'),
                filter_name=data.get('filter_name'),
            )
        else:
            filter_requirement = requirementFilter.objects.filter(
                parent_tab__user_id=data.get('user_id'),
                parent_tab__tab_name=data.get('parent_tab_name'),
            )
        serializer = self.serializer_class(filter_requirement, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        filter_id = request.data.get('id')
        print(filter_id)
        try:
            filter = requirementFilter.objects.get(pk=filter_id)
            filter.delete()
        except filter.DoesNotExist:
            raise APIException("Filter does not exist")
        return Response({'data': {'message': 'Delete success'}}, status=status.HTTP_200_OK)


class FilterRequirementUpdateView(generics.GenericAPIView):
    serializer_class = FilterRequirementUpdateSerialize
    renderer_classes = [CustomRenderer]

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')

        if not user_id or not parent_tab_name:
            return Response({'exception': 'user_id and parent_tab_name are required for receiving single filter'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            filter = serializer.update(serializer)
        except Exception as e:
            return Response({'data': None, 'exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': filter}, status=status.HTTP_201_CREATED)


class TestcaseUpdateView(generics.GenericAPIView):
    serializer_class = TestCaseUpdateSerialize
    renderer_classes = [CustomRenderer]

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')
        if not user_id or not parent_tab_name:
            return Response({'exception': 'user_id and parent_tab_name are required for receiving single filter'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            subtab = serializer.update(serializer)
        except Exception as e:
            return Response({'data': None, 'exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': subtab}, status=status.HTTP_200_OK)


class subTabSearchView(generics.GenericAPIView):
    serializer_class = CreateTestcaseListSerializer
    renderer_classes = [CustomRenderer]

    def get_queryset(self):
        data = self.request.GET
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')
        filter_name = data.get('filter_name')
        req_id = data.get('req_id')
        if not filter_name and not req_id :
            query_set = subTab.objects.filter(parent_tab__user_id=user_id,
                                              parent_tab__tab_name=parent_tab_name,)
        elif not filter_name :
            query_set = subTab.objects.filter(parent_tab__user_id=user_id,
                                              parent_tab__tab_name=parent_tab_name, req_id__in=req_id.split(','))
        elif not req_id :
            req_filter = requirementFilter.objects.get(filter_name=filter_name, parent_tab__tab_name=parent_tab_name)
            query_set = subTab.objects.filter(parent_tab__user_id=user_id,
                                              parent_tab__tab_name=parent_tab_name, req_id__in=req_filter.req_id.split(','))
        else:
            req_filter = requirementFilter.objects.get(filter_name=filter_name, parent_tab__tab_name=parent_tab_name)
            query_set = subTab.objects.filter(parent_tab__user_id=user_id,
                                              parent_tab__tab_name=parent_tab_name, req_id__in=req_filter.req_id.split(','), req_id__icontains=req_id)

        return query_set

    def get(self, request):
        data = request.GET
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')
        if not user_id or not parent_tab_name:
            return Response({'exception': 'user_id and parent_tab_name are required for receiving single filter'}, status=status.HTTP_400_BAD_REQUEST)
        list_testcase = self.get_queryset()
        serializers = self.serializer_class(list_testcase, many=True)

        return Response({'data': serializers.data}, status=status.HTTP_200_OK)
    
class GetAllFilterView(generics.GenericAPIView):
    
    renderer_classes= [CustomRenderer]
    
    def get(self, request):
        data = request.GET
        
