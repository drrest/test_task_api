from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Post
        fields = ('id', 'title', 'text', 'user')
        extra_kwargs = {}


class LikesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Post
        fields = ('post', 'user')
        extra_kwargs = {}
