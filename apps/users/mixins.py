# from django.http import JsonResponse
from rest_framework import status
import datetime
from config.helpers.utils import error_response
from .models import User


class CustomLoginRequiredMixin():

    def dispatch(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return error_response('Please set Auth Token.', status.HTTP_401_UNAUTHORIZED)

        token = request.headers.get('Authorization')
        now = datetime.datetime.now()

        login_user = User.objects.filter(
            token=token,
            token_expires__gt=now)
        if len(login_user) == 0:
            return error_response('The token is invalid or expired.', status.HTTP_401_UNAUTHORIZED)
        
        request.login_user = login_user[0]
        return super().dispatch(request, *args, **kwargs)



        # ).first()

        # if not login_user:
        #     return JsonResponse(
        #         {'error': 'The token is invalid or expired.'},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )

        # request.login_user = login_user
        # return super().dispatch(request, *args, **kwargs)