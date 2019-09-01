# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jwt
from django.contrib.auth.base_user import BaseUserManager
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin)
from rest_framework.exceptions import ValidationError

from test_task_api import settings

'''
    Refresh token mechanic SKIPPED
'''


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
 
    """
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @classmethod
    def get_current_user(self, request, updated_request=True):
        '''
            Can be used to extends current request with current user data

        :param updated_request:     - Will return updated object of "request" on True value.
                                      Else will return just User object
        :param request:             - 'request' object in views
        :return:
        '''
        token = request.META.get('HTTP_AUTHORIZATION', " ").split('  ')[1]
        try:
            valid_data = jwt.decode(token, settings.SECRET_KEY)
            user_object = User.objects.filter(email=valid_data['username']).pk
            request.user = user_object
        except ValidationError as v:
            print("validation error", v)
        if updated_request:
            return request
        else:
            return user_object

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
