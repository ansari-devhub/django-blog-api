from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Category : {self.name}'
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
class Post(models.Model):
    STATUS_TYPES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_TYPES,
        default='draft'
    )
    views = models.PositiveBigIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_posts')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category_posts'
    )
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Post by {self.owner.username if self.owner else "Deleted User"}'
    
class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
        blank=True,related_name='author_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author.username if self.author else "Deleted User"}'
    