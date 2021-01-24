from django.urls import path, include
from . import views
from .views import PostViewSet ,RegisterView, CommentView, ProfileView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('PostApi',PostViewSet, basename='PostApi')
router.register('RegisterApi',RegisterView, basename='RegisterApi')
router.register('CommentApi',CommentView, basename='CommentApi')
router.register('ProfileApi',ProfileView, basename='ProfileApi')

urlpatterns = [

        path('',include(router.urls)),

]