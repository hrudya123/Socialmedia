
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated,AllowAny
from socialmedia_app.models import Post, Comment, Like
from socialmedia_app.serializers import *


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Post.objects.get(pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)

        if post.owner != request.user:
            return Response({"detail": "You cannot edit another user's post."},status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = self.get_object(pk)
        if post.owner != request.user:
            return Response({"detail": "You cannot edit another user's post."},status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.owner != request.user:
            return Response({"detail": "You cannot delete another user's post."},status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all().order_by("-added_at")
        post_id = request.query_params.get("post_object")
        if post_id:
            comments = comments.filter(post_object_id=post_id)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LikeListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        likes = Like.objects.all().order_by("-created_at")
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.validated_data["post_obj"]
            existing_like = Like.objects.filter(owner=request.user,post_obj=post).exists()
            if existing_like:
                return Response({"detail": "You have already liked this post."},status=status.HTTP_400_BAD_REQUEST)
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LikeDeleteView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        like = Like.objects.get(pk=pk,owner=request.user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

