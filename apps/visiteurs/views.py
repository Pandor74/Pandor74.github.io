from django.shortcuts import render,redirect
from django.urls import re_path

# Create your views here.

def home(request):
	return render(request,'visiteurs/base.html')




