from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Author, Post, Comment
from .serializers import PostSerializer, CommentSerializer, SignupSerializer

# Create your views here.

class PostListCreateView(APIView):
    

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]

        return [AllowAny()]

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def post(self, request):
        author = get_object_or_404(
            Author,
            user=request.user
        )

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            post = serializer.save(author=author)

            return Response(
                PostSerializer(post).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PostCommentsView(APIView):
   

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]

        return [AllowAny()]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        comments = post.comments.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        author = get_object_or_404(
            Author,
            user=request.user
        )

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(
                post=post,
                author=author
            )

            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class ReadinessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ready"})


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )