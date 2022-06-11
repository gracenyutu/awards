from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    return render(request, 'awwards/home.html')

def Login(request):
    return render(request, 'registration/login.html')