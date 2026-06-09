from django.urls import path
from .views import *

urlpatterns = [
    path('posts/',PostListView.as_view()),
    path('posts/<int:id>/', PostDetailView.as_view()),
    path('posts/<str:cat_name>/', PostCreateView.as_view()),
    path('posts/<int:id>/comments', PostCommentsView.as_view()),
    path('categories/', CategoryListView.as_view())
]