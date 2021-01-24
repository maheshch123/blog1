from django.urls import path
from . import views
from . views import UserPostListView, PostDetailView, PostDeleteview, PostCreateView, PostUpdateView,CommentUpdateView

urlpatterns = [
    path('base',views.base, name='base'),
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('index',views.index, name='index'),
    path('logout',views.logout, name='logout'),
    path('profile',views.profile, name='profile'),
    

    path('profile_update', views.profile_update, name='profile_update'),
    path('user/<str:username>', UserPostListView.as_view(), name='user_posts'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post_details' ),
    path('post/<int:pk>/delete/',PostDeleteview.as_view(), name='post_delete' ),
    
    path('profile_posts',views.profile_posts, name='profile_posts'),
    path('post/new/',PostCreateView.as_view(), name='post-create' ),
    path('post_update',views.post_update, name='post_update'),
    path('post/<int:pk>/update',PostUpdateView.as_view(), name='post-update' ),
    
    path('comment_update/<int:id>',views.comment_update, name='comment_update'),
    path('comment/<int:pk>/update',CommentUpdateView.as_view(), name='comment-update' ),
    path('delete/<int:id>',views.delete, name='delete'),
    path('ApiKey',views.APiKey, name='ApiKey')

]

