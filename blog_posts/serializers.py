from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = [
            'post',
            'author',
            'created_at'
        ]
        fields = [
            'content',
            'post',
            'author',
            'created_at'
        ]
        
class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many = True, read_only = True)
    post_comments = CommentSerializer(many = True, read_only = True)
    short_content = serializers.SerializerMethodField(read_only = True)
    comment_count = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Post
        read_only_fields = [
            'slug',
            'views',
            'owner',
            'category',
            'created_at',
            'updated_at',
        ]
        fields = [
            'title',
            'views',
            'category',
            'owner',
            'created_at',
            'updated_at',
            'content',
            'status',
            'tags',
            'post_comments',
            'short_content',
            'comment_count',
        ]
        
    def get_short_content(self, obj):
        return obj.content[:151]
        
    def get_comment_count(self, obj):
        return obj.post_comments.count()
        
    def validate_title(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                'Title too short'
            )
        return value
    
    def validate(self, attrs):
        if attrs.get('status') == 'published' and len(attrs.get('content','').replace(" ","")) <= 5:
            raise serializers.ValidationError('Content too short')
        return attrs