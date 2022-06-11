from django.shortcuts import render, redirect
from .forms import SignupForm, ReviewForm
from django.contrib.auth import login, authenticate
from .models import Profile, Post, Review
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import ProfileSerializer, UserSerializer, PostSerializer
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    return render(request, 'awwards/home.html')

def Login(request):
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
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
        return render(request, 'results.html', context)
    else:
        message = "You haven't searched for any site"
    return render(request, 'search.html', {'message': message})

@login_required(login_url='Login')
def site(request, post):
    post = Post.objects.get(title=post)
    ratings = Review.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Review.objects.filter(post=post)

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
        form = ReviewForm()
    context = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'site.html', context)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer