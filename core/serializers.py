from sqlite3 import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, APIException, NotFound
import logging

from rest_framework import serializers
from .models import *


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            user = User()
            user.password = validated_data["password"]
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
        fields = ('username', 'id')

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
        fields = ('password', 'username')

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = User.objects.filter(username=username, password=password)

        if not user:
            raise AuthenticationFailed(
                'User and password are invalid, try again!')

        return {
            'id': user.values('id').get()['id'],
            'username': user.values('username').get()['username']
        }


class LogOutAPISerializer(serializers.Serializer):

    def validate(self, attrs):
        return attrs


class CreateTestcaseSerializer(serializers.ModelSerializer):
    req_id = serializers.CharField(max_length=255, required=True)
    testcase_id = serializers.CharField(max_length=255, required=True)
    testcase_result = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = subTab
        fields = ('id', 'testcase_id', 'req_id',
                  'testcase_result', 'parent_tab')
        
    def validate(self, data):
        testcase_id = data.get('testcase_id',None)
        req_id = data.get('req_id',None)

        try:
            obj = self.Meta.model.objects.get(testcase_id=testcase_id, req_id=req_id)
        except self.Meta.model.DoesNotExist:
            return data
        if self.instance and obj.id == self.instance.id:
            return data
        else:
            raise serializers.ValidationError('testcase_id with req_id already exists')

    def create(self, validated_data):
        req_id = validated_data.get('req_id', None)
        testcase_id = validated_data.get('testcase_id', None)
        testcase_result = validated_data.get('testcase_result', None)
        parent_tab_name = validated_data.get('parent_tab_name', None)
        user_id = validated_data.get('user_id')
        
        parent_tab_id = ParentTab.objects.get(user_id=user_id, tab_name=parent_tab_name)

        return subTab.objects.create(
            req_id=req_id,
            testcase_id=testcase_id,
            testcase_result=testcase_result,
            parent_tab_id=parent_tab_id.id         
        )     

class CreateTestcaseListSerializer(serializers.ListSerializer):
    class Meta:
        ...


class FilterRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = requirementFilter
        fields = ('id', 'req_id', 'filter_name')
        
    def create(self, validated_data):
        data = self.initial_data
        user_id = data.get('user_id')
        parent_tab_name = data.get('parent_tab_name')
        req_id = data.get('req_id')
        filter_name = data.get('filter_name')
        try:
            parent_tab = ParentTab.objects.get(user_id=user_id, tab_name=parent_tab_name)
        except ParentTab.DoesNotExist:
            raise APIException("parent tab does not exist")
        requirementFilter.objects.create(
            parent_tab_id=parent_tab.id,
            req_id=req_id,
            filter_name=filter_name,
        )
        return data

class FilterRequirementUpdateSerialize(serializers.ModelSerializer):
    class Meta:
        model = requirementFilter
        fields = ('id', 'req_id', 'filter_name', 'parent_tab_id')
        
    def validate(self, attrs):
        data = self.initial_data
        filter_id = data.get('id')
        try:
            return requirementFilter.objects.get(pk=filter_id)
        except requirementFilter.DoesNotExist as e :
            raise NotFound(f"{e}") from e
        
    def update(self, validated_data):
        data = self.initial_data
        id = data.get('id')
        req_id = data.get('req_id')
        filter_name = data.get('filter_name')
        filter = requirementFilter.objects.get(pk=id)
        filter.filter_name = filter_name
        filter.req_id = req_id
        filter.save()
        return data