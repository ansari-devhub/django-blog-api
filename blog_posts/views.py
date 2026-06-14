from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)

from blog_posts.pagination import *


from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
class PostListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    
    
    filterset_fields = [
        'status',
        'category',
    ]
    
    search_fields = [
        'title',
        'content',
    ]
    
    ordering_fields = [
        'views',
        'created_at',
    ]
    
class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        category = get_object_or_404(Category, name = self.kwargs['cat_name'])
        serializer.save(
            owner = self.request.user,
            category = category
        )
        
    
class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
        
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
class PostCommentsView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get(self, request, id):
        comments = Comment.objects.filter(post_id = id)
        serializer = CommentSerializer(comments,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, id):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(
                post_id = id,
                author = request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryCursorPagination