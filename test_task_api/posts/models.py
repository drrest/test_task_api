# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from threading import local

from users.models import User

_thread_locals = local()

from django.db import models

from test_task_api import settings

class Post(models.Model):
    # Fields
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    text = models.TextField(max_length=1000)
    draft = models.BooleanField(default=False)

    '''
       I think it doesn't needed in this case to realize mechanic of 
       gathering users who like, and unlike. But this task can be solved 
       with ManyToMany relations in both cases
    '''
    likers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liker",
    )

    unlikers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="unliker",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete="cascade",
        related_name="posts",
    )


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.text

    def save(self, *args, **kwargs):

        super(Post, self).save(*args, **kwargs)
