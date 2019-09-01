# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jwt
# Create your views here.
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

import users
from posts.models import Post
from posts.serializer import PostSerializer, LikesSerializer
from test_task_api import settings
from django.core import serializers
from users.models import User


class Utility:

    @classmethod
    def get_current_user(cls, request, updated_request=True):
        """
            Can be used to extends current request with current user hata
        :param updated_request:     - Will return updated object of "request" if it True value.
                                      Else will return just User object
        :param request:             - 'request' object in views
        :return:
        """

        # gxtracting encoded JWT token directly from header as a string()
        token = request.META.get('HTTP_AUTHORIZATION', " ").split('  ')[1]

        # need to be initiated, cause of possibility
        user_id = None
        try:
            # decoding of jwt encoded token
            jwt_decoded = jwt.decode(token, settings.SECRET_KEY)
            # find for user_id with the key 'email'
            user_id = User.objects.get(email=jwt_decoded['email'])
            # Update 'request' with 'user' data
            request.data['user'] = user_id
        except ValidationError as v:
            print("validation error", v)
        if updated_request:
            return request
        else:
            return user_id

    @classmethod
    def get_likers_count(cls, post_id):
        return Post.objects.get(pk=post_id).likers.all().count()

    @classmethod
    def get_unlikers_count(cls, post_id):
        return Post.objects.get(pk=post_id).unlikers.all().count()


class CreatePostAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    @staticmethod
    def post(request):
        post = request.data
        output = {}
        serializer = PostSerializer(data=post)

        try:
            user_object = Utility.get_current_user(request, updated_request=False)
            post['user'] = user_object.pk
            serializer.is_valid(raise_exception=True)
            serializer.save()

            output['answer'] = "ok"
            status_type = status.HTTP_201_CREATED
        except ValidationError as exception:
            output['answer'] = {"error": {"status_code": str(exception.status_code),
                                          "status_details": str(exception.default_detail),
                                          "status_message": exception.get_full_details()}}
            status_type = status.HTTP_400_BAD_REQUEST
        return Response({"response": output}, status=status_type)

class ListOfPostsAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    @staticmethod
    def get(request):
        output = {}

        try:
            posts = Post.objects.filter(draft=False)
            serialize = json.loads(serializers.serialize("json", posts))
            output['answer'] = [{"pk":post['pk'],"meta":post['fields']} for post in serialize]

            status_type = status.HTTP_201_CREATED
        except ValidationError as exception:
            output['answer'] = {"error": {"status_code": str(exception.status_code),
                                          "status_details": str(exception.default_detail),
                                          "status_message": exception.get_full_details()}}
            status_type = status.HTTP_400_BAD_REQUEST
        return Response({"response": output}, status=status_type)


class LikePostAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = LikesSerializer

    @staticmethod
    def post(request):
        output = ""
        # This is lock key to stop in progress when some error
        lock_next_step = False
        like_data = request.data
        user_object = Utility.get_current_user(request, updated_request=False)
        user_id = user_object.pk
        post_id = like_data['post']

        post_to_update = None

        try:
            # Try to fine post for updating
            post_to_update = Post.objects.get(pk=post_id)
        except users.models.User.DoesNotExist:
            # output text
            output = "Post #{id} doesnt exists".format(id=post_id)
            # return
            lock_next_step = True

        # if next step allowed
        if not lock_next_step:
            try:
                # check if liker doesnt like this post yet
                post_to_update.likers.get(pk=user_id)  # Raise exception if doesn't exists )
                # if does - he cannot like again - so stop
                output = "User {email} already liked this post".format(email=user_object.email)
            except users.models.User.DoesNotExist:
                # if doesnt ->
                # remove user from unlikers, cause of like
                post_to_update.unlikers.remove(user_id)
                # add user into likers
                post_to_update.likers.add(user_id)
                # save
                post_to_update.save()

                # get likers count
                likes = Utility.get_likers_count(post_to_update.pk)
                # get unlikers count
                unlikes = Utility.get_unlikers_count(post_to_update.pk)

                # form out
                output = {"answer": "ok",
                          "likes": likes,
                          "unlikes": unlikes
                          }

        return Response({"response": output}, status=status.HTTP_202_ACCEPTED)


# Out of commentary about this class - is the same
# The best way is Abstract class and 2 child
class UnlikePostAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = LikesSerializer

    @staticmethod
    def post(request):
        output = ""
        lock_next_step = False
        like_data = request.data
        user_object = Utility.get_current_user(request, updated_request=False)
        user_id = user_object.pk
        post_id = like_data['post']

        post_to_update = None

        try:
            post_to_update = Post.objects.get(pk=post_id)
        except users.models.User.DoesNotExist:
            output = "Post #{id} doe's not exists".format(id=post_id)
            lock_next_step = True

        if not lock_next_step:
            try:
                post_to_update.unlikers.get(pk=user_id)  # Raise exception if doesn't exists )
                output = "User {email} already liked this post".format(email=user_object.email)
            except users.models.User.DoesNotExist:
                post_to_update.likers.remove(user_id)
                post_to_update.unlikers.add(user_id)
                post_to_update.save()

                likes = Utility.get_likers_count(post_to_update.pk)
                unlikes = Utility.get_unlikers_count(post_to_update.pk)

                output = {"answer": "ok",
                          "likes": likes,
                          "unlikes": unlikes
                          }

        return Response({"response": output}, status=status.HTTP_202_ACCEPTED)
