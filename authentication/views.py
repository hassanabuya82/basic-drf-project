import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import  Group
from myauth.models import CustomUser as User
from django.core.mail import EmailMessage
from django.db.models import query
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins,generics
from rest_framework.views import APIView
from .serializers import *



from .models import ActivateToken,  ResetToken


class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'key': token.key,
            'user_id': user.pk,
            # 'group': user.groups.all()[0].id
        })


class Register(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = []


@api_view(["POST"])
def activate_reset(request):
    data = request.data
    email = data['email']

    try:
        user = User.objects.get(email=email)
        code, created = ActivateToken.objects.get_or_create(user=user)
        if code.expiry < timezone.now():
            code.delete()
            ActivateToken.objects.get_or_create(user=user)

        print('sending', code.token)
        send_email(email, code.token,"activate")
        return Response(status=status.HTTP_200_OK)

    except Exception:
        return Response({'error': "user with that email does not exist"}, status=status.HTTP_403_FORBIDDEN)

class ActivateAccount(generics.CreateAPIView):
    serializer_class = AccountActivateSerializer
    permission_classes = []

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = serializer.save()
            return Response(TokenSerializer(token).data,status=status.HTTP_201_CREATED)





class ResetActivate(generics.CreateAPIView):
    serializer_class = ResetActivateSerializer
    permission_classes = []

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            msg = serializer.save()
            return Response({"details":"Success"},status=status.HTTP_201_CREATED)



@api_view(['POST'])
def pass_reset(request):
    data = request.data
    email = data['email']

    try:
        user = User.objects.get(email=email)
        code, created = ResetToken.objects.get_or_create(user=user)
        if code.expiry < timezone.now():
            code.delete()
            ResetToken.objects.get_or_create(user=user)

        print('sending', code.token)
        send_email(email, code.token,"reset")
        return Response(status=status.HTTP_200_OK)

    except Exception:
        return Response({'error': "user with that email does not exist"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def reset_confirm(request):
    data = request.data
    email = data['email']
    code = int(data['code'])

    user = User.objects.get(email=email)
    try:
        kode = ResetToken.objects.get(user=user)
    except Exception:
        return Response({'error':"code is not valid"}, status=status.HTTP_403_FORBIDDEN)

    if kode.expiry < timezone.now():
        return Response({'error': 'code has expired'}, status=status.HTTP_403_FORBIDDEN)

    if kode.token == code:
        kode.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'key': token.key,
            'user_id': user.pk,
            # 'group': user.groups.all()[0].id
        })
    else:
        return Response({'error': 'code is not valid'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password(request):
    user = request.user
    data = request.data
    oldPass = data['oldPass']
    newPass = data['newPass']

    if user.password is not oldPass:
        return Response(status.HTTP_401_UNAUTHORIZED)
    
    user.password = newPass
    user.save()

    print("password after", user.password)

    return Response(status=status.HTTP_201_CREATED)



