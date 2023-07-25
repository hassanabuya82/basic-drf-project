import contextlib
from .serializers import UserCreationSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


class MyProfile(APIView):
    def get(self, request):
        user = request.user
        return Response(data={
            'names': f'{user.first_name} {user.last_name}',
            'email': user.email
        }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def list_groups(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        serialized_groups = serializer.data

        return Response(serialized_groups)

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_group_list_view(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serialized_users = []

        for user in users:
            groups = user.groups.all()
            serialized_user = UserSerializer(user).data
            serialized_user['groups'] = GroupSerializer(groups, many=True).data
            serialized_users.append(serialized_user)

        return Response(serialized_users)

    elif request.method == 'POST':
        user_ids = request.data.get('user_id')
        group_id = request.data.get('group_id')


        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        
        for user_id in user_ids:
            with contextlib.suppress(Exception):
                user = CustomUser.objects.get(pk=user_id)
                user.groups.clear()
                user.groups.add(group)
    
        return Response({'message': 'User added to group successfully'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def user_list_create(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def technician_list(request):
    if request.method == 'GET':
        group_name = 'Technician'
        group = Group.objects.filter(name=group_name).first()

        if group:
            users = CustomUser.objects.filter(groups=group)
            serializer = TechnicianSerializer(users, many=True)
            return Response(serializer.data)

        return Response([])
