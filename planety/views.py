from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Comment
from . import views
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User, auth

from django.contrib.auth.decorators import login_required
################################################
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm, ProfileUpdateForm, NewCommentForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.
def base(request):

    return render(request,'base.html')

####################################################

def index(request):
    posts = Post.objects.all().filter(created_date__lte=timezone.now()).order_by('-created_date') # displays posts descending order
    user =request.user
    context={
        'posts' : posts,
        'user' : user,
    }
    return render(request,'index.html',context)



####################################################

def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect ('register')
                print("user name taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return redirect('register')
            else:    
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                print("user created")
                          
        else:
            print("password not matching...")
            messages.info(request, "password not matching")
            return redirect('register')
        return redirect('index')

    else:
        return render(request,'register.html')


    return render(request,'register.html')

################################################

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "invalild username or password")
            return redirect('base')
    else:
        return render(request, 'base.html')

##############################################
        
def logout(request):
    auth.logout(request)
    return redirect('/index')


#############################################


##############################################
# profile page

def profile(request):

    return render(request,'profile.html')

################################################
#profile update 

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'profile details updated successfully')
            return render(request,'profile.html')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request,'profile_update.html',context)

################################
# admin posts posts

class UserPostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name ='posts'
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_date')

################################
# post details page

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)

#############################
# for delete post

class PostDeleteview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = ('/')
    template_name = 'post_delete.html'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
##############################
# for creating post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['image','caption']
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
############################
# for post update 

def post_update(request):
    return render(request,'post_update.html')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['image','caption']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

############################
# profile posts

def profile_posts(request):
    user = request.user
    
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    return render(request,'profile_posts.html',{'posts':posts, 'user':user})

#####################################


#######################
# comments update

def comment_update(request):
    data = Comment.objects.get(id=id)
    return render(request,'comment_update.html',{'data':data}) 


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'comment_update.html'
    fields = ['content']
    success_url = '/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False
    
    
###########################
# comment delete

def delete(request,id):
    comments = Comment.objects.get(id=id).delete()
    return redirect('/')

def APiKey(request):
    return render(request,'APiKey.html')