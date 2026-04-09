# from .models import User
# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password, check_password
# from django.utils import timezone
# from secrets import token_hex
# import datetime
# # import uuid


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'token', 'token_expires')


# class UserSignUpSerializer(serializers.ModelSerializer):
#     email = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True)
#     token = serializers.CharField(read_only=True)
#     token_expires = serializers.DateTimeField(read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'password', 'token', 'token_expires')

#     def create(self, validate_data):

 
#         if User.objects.filter(email=validate_data['email']).exists():
#             raise serializers.ValidationError({
#                 'email': ['This email is already taken']
#             })

#         validate_data['password'] = make_password(validate_data['password'])

#         # generate token
#         validate_data['token'] = token_hex(30)
#         validate_data['token_expires'] = timezone.now() + datetime.timedelta(days=7)

#         return super().create(validate_data)


# class UserSignInSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     name = serializers.CharField(read_only=True)
#     token = serializers.CharField(read_only=True)
#     token_expires = serializers.DateTimeField(read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'password', 'token', 'token_expires')
 

#     def create(self, validate_data):
#         user = User.objects.filter(email=validate_data['email'])

#         if len(user) and check_password(validate_data['password'], user[0].password):
#             user = user[0]
#             user.token = str(uuid.uuid4())
#             user.token_expires = timezone.now() + datetime.timedelta(days=1)
#             user.save()
#             return user

#         raise serializers.ValidationError({
#             "error": "The password or email is incorrect."
#         })

from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from secrets import token_hex
import datetime
import uuid   # ✅ FIX 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'token', 'token_expires')


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)
    token_expires = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'token', 'token_expires')

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({
                'email': ['This email is already taken']
            })

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['token'] = token_hex(30)
        validated_data['token_expires'] = timezone.now() + datetime.timedelta(days=7)

        return super().create(validated_data)


class UserSignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    token_expires = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'token', 'token_expires')

    def create(self, validated_data):  # ✅ FIX 2
        user = User.objects.filter(email=validated_data['email']).first()  # ✅ FIX 3

        if user and check_password(validated_data['password'], user.password):
            user.token = str(uuid.uuid4())
            user.token_expires = timezone.now() + datetime.timedelta(days=1)
            user.save()
            return user

        raise serializers.ValidationError({
            "error": "The password or email is incorrect."
        })