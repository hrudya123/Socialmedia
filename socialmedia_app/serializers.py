from rest_framework import serializers
from django.contrib.auth.models import User
from socialmedia_app.models import Post, Comment, Like


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at"]


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id", "added_at", "owner"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["id", "created_at", "owner"]
