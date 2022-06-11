from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login, authenticate

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
    return render(request, 'registration/signup.html', {'form': form})