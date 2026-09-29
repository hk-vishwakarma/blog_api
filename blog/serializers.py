
from rest_framework import serializers
from .models import *


from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Author, Post, Comment


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        Author.objects.create(user=user)

        return user

class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Author
        fields = ["id", "username", "bio"]


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]