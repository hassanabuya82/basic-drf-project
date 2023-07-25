from wsgiref import validate
from django.contrib.auth.models import Group
from django.forms import ValidationError
from django.http import JsonResponse
from myauth.models import CustomUser as User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from authentication.models import ActivateToken
from .utils import TokenTemplate, send_email
from rest_framework import serializers, status

from rest_framework.response import Response

from rest_framework.exceptions import APIException


class UnauthorizedValidator(APIException):
    status_code = 403
    default_detail ='Unauthorized'


class NotFoundValidator(APIException):
    status_code = 404
    default_detail ='Unauthorized'


class UserDetailSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','profile')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
        read_only_fields = ['user','created']
        # depth = 2

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        # fields = ['id','name',]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email','id','groups','first_name','last_name']

    def create(self,validated_data):
        groups = validated_data.pop('groups')
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True},
            'email':{'required':True},
            'password':{'write_only':True}
        }
      

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        email = validated_data['email']
        otp = ActivateToken.objects.create(user=user)
        user.is_active=False
        user.save()

        temp = TokenTemplate(otp.token,'Activation')

        send_email(recepient=[email],subject=temp['subject'],message=temp['message'])

        return user





class AccountActivateSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    otp = serializers.IntegerField(write_only=True)

    def create(self,validated_data):
        email = validated_data['email']
        otp = validated_data['otp']
        try:
            user = User.objects.get(email=email)
            activation = user.activate_token
            if  activation.status != 'active' or activation.token != otp:
                raise serializers.ValidationError('Expiry',code=403)
            activation.delete()
            user.is_active=True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return token
        except Exception as e:
            if e.args[0] =='Expiry':
                raise UnauthorizedValidator('Token Expired') from e
            raise NotFoundValidator('User Not Found') from e





class ResetActivateSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self,validated_data):
        email = validated_data['email']
        try:
            user = User.objects.get(email=email)
            # if activation := user.activate_token:
            #     activation.delete()
            ActivateToken.objects.filter(user=user).delete()
            otp = ActivateToken.objects.create(user=user)


            temp = TokenTemplate(otp.token,'reset')
            
            send_email(recepient=[user.email],subject=temp['subject'],message=temp['message'])
            return "success"
        except Exception as e:
            print(e)
            raise NotFoundValidator('User Not Found') from e
