from django.shortcuts import render
from rest_framework import viewsets
from planety.models import Post,Comment,Profile
from .serializers import PostSerializers,UserCreateSearilizer,CommentSerializers, ProfileSerializers
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('author',)


User = get_user_model()
# class UserCreareApiView(CreateAPIView):
#     serializer_class = UserCreateSearilizer
#     queryset = User.objects.all()
    
class RegisterView(viewsets.ModelViewSet):
    serializer_class = UserCreateSearilizer
    queryset = User.objects.all()

class CommentView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializers
    queryset = Comment.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('author',)

class ProfileView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('user',)