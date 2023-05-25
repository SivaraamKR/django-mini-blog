from django.shortcuts import render, HttpResponseRedirect
from .forms import  SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from datetime import datetime
# Create your views here.
def home(request):
    user = request.user
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts, 'user':user})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations you are an Author!!' )
            form.save()
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
            

        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
              
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
def delete_post(request, id):
    if request.user.is_authenticated:
         if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')