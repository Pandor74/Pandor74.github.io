from django.shortcuts import render,redirect


def home_redirection(request):
	return redirect('/visiteurs')