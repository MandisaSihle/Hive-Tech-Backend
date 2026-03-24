from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from secrets import token_hex
import datetime
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'token', 'token_expires')


class UserSignUpSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)
    token_expires = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'token', 'token_expires')

    def create(self, validated_data):

        # ✅ FIXED "=" (you had "-")
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({
                'email': ['This email is already taken']
            })

        # hash password
        validated_data['password'] = make_password(validated_data['password'])

        # generate token
        validated_data['token'] = token_hex(30)
        validated_data['token_expires'] = timezone.now() + datetime.timedelta(days=7)

        return super().create(validated_data)


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'token', 'token_expires')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email'])

        if len(user) and check_password(validated_data['password'], user[0].password):
            user = user[0]
            user.token = str(uuid.uuid4())
            user.token_expires = timezone.now() + datetime.timedelta(days=1)
            user.save()
            return user

        raise serializers.ValidationError({
            "error": "The password or email is incorrect."
        })