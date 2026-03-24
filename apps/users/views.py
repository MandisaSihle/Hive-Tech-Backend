from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from apps.users.mixins import CustomLoginRequiredMixin
from .models import User
from .serializers import UserSerializer, UserSignInSerializer, UserSignUpSerializers


class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializers


class UserSignIn(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignInSerializer


class UserProfile(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer([request.login_user], many=True)
        return Response(serializer.data)