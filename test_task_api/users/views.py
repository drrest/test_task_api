# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Components
import jwt
from django.contrib.auth import user_logged_in
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

# Internal
import users
from test_task_api import settings
from users.models import User
from users.serializers import UserSerializer

# CleatBit section
import clearbit
from test_task_api.settings import CLEARBIT_KEY

clearbit.key = CLEARBIT_KEY


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        output = {}
        try:
            user = request.data

            # check user with clearbit
            # response = clearbit.Enrichment.find(email=user['email'], stream=True)
            # if response:
            #     #Make some action with received data
            #     pass

            serializer = UserSerializer(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            output['answer'] = serializer.data
        except ValidationError as exception:
            output['answer'] = {"error": {"status_code": str(exception.status_code),
                                          "status_details": str(exception.default_detail),
                                          "status_message": exception.get_full_details()}}

        return Response({"response": output}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        # .get method will raise DoesNotExist
        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {'name': "%s %s" % (
                    user.first_name, user.last_name), 'token': token}
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except users.models.User.DoesNotExist:
        res = {'error': 'There are no any users with these credentials'}
        return Response(res, status=status.HTTP_403_FORBIDDEN)
