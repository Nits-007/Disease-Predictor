from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib import messages
# Create your views here.

@unauthenticated_user
def user_login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        print(email)
        password=request.POST.get('password')
        print(password)
        our_user=authenticate(email=email,password=password)
        print(our_user)
        if our_user is not None:
            login(request,our_user)
            return redirect('/')
        print("login failed")
        messages.info(request,"Login failed")
    return render(request,'login.html')

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('/')