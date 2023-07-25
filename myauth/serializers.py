from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.serializers import *
from django.contrib.auth.models import Permission
from .models import *
from rest_framework.response import Response
from rest_framework import status, serializers


class UserSerializer(ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']


class GroupSerializer(serializers.ModelSerializer):
    # permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name']


class TechnicianSerializer(ModelSerializer):
    full_name = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'groups']


class CustomUserSerializer(ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class CustGroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'users']
