

# from rest_framework import status
# import datetime

# from config.helpers.error_response import error_response
# from .models import User

# # Add this mixin to the login-required classes.


# class CustomLoginRequiredMixin():

#     def dispatch(self, request, *args, **kwargs):
#         if 'Authorization' not in request.headers:
#             return error_response('Please set Auth-Token.', status.HTTP_401_UNAUTHORIZED)

#         token = request.headers['Authorization']
#         now = datetime.datetime.now()
#         login_user = User.objects.filter(token=token, token_expires__gt=now)
#         if len(login_user) == 0:
#             return error_response('The token is invalid or expired.', status.HTTP_401_UNAUTHORIZED)

#         request.login_user = login_user[0]
#         return super().dispatch(request, *args, **kwargs)

# from rest_framework import status
# from rest_framework.response import Response
# import datetime

# from config.helpers.error_response import error_response
# from .models import User


# class CustomLoginRequiredMixin:
#     def dispatch(self, request, *args, **kwargs):
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return error_response(
#                 "Please set Auth-Token.",
#                 status.HTTP_401_UNAUTHORIZED
#             )

#         token = auth_header.strip()
#         now = datetime.datetime.now()

#         login_user = User.objects.filter(
#             token=token,
#             token_expires__gt=now
#         ).first()

#         if login_user is None:
#             return error_response(
#                 "The token is invalid or expired.",
#                 status.HTTP_401_UNAUTHORIZED
#             )

#         request.login_user = login_user
#         return super().dispatch(request, *args, **kwargs)

from rest_framework import status
from django.utils import timezone

from config.helpers.error_response import error_response
from .models import User


class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return error_response(
                "Please set Auth-Token.",
                status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.strip()
        now = timezone.now()

        login_user = User.objects.filter(
            token=token,
            token_expires__gt=now
        ).first()

        if login_user is None:
            return error_response(
                "The token is invalid or expired.",
                status.HTTP_401_UNAUTHORIZED
            )

        request.login_user = login_user
        return super().dispatch(request, *args, **kwargs)