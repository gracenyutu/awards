from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, RatingForm, PostForm, UpdateUserForm, UpdateUserProfileForm
from django.contrib.auth import login, authenticate
from .models import Profile, Post, Rating
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from django.contrib import messages
import requests

# Create your views here.
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    try:
        posts = Post.objects.all()
        posts = posts[::-1]
        a_post = random.randint(0, len(posts)-1)
        random_post = posts[a_post]
        print(random_post.photo)
    except Post.DoesNotExist:
        posts = None

    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'awwards/home.html',{'posts': posts, 'form': form, 'random_post': random_post})



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

def search(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        results = Post.objects.filter(title__icontains=title).all()
        print(results)
        message = f'name'
        context = {'results': results,'message': message}
        return render(request, 'awwards/search.html', context)
    else:
        message = "You haven't searched for any site"
    return render(request, 'awwards/search.html', {'message': message})

@login_required(login_url='Login')
def site(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return redirect(request.path_info)
    else:
        form = RatingForm()
    context = {
        'id' : id,
        'post': post,
        'rating_form': form,
        'rating_status': rating_status
    }
    return render(request, 'awwards/site.html', context)

@login_required(login_url='Login')
def profile(request, username):
    return render(request, 'awwards/profile.html')

def user_profile(request, username):
    userprof = get_object_or_404(User, username=username)
    if request.user == userprof:
        return redirect('profile', username=request.user.username)
    context = {
        'userprof': userprof,
    }
    return render(request, 'awwards/userprofile.html', context)

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'awwards/edit.html', context)

@login_required(login_url='login')
def upload(request):
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_pic.url
    if request.method == 'POST':
        post = request.FILES['post']
        print(post)
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.create(user=request.user,photo=post)
        if posts:
            messages.success(request,"post uploaded successfully!")
        else:
            messages.success(request,"post failed!")
    return render(request,'awwards/uploadpost.html',{'profileimage':profileimage})