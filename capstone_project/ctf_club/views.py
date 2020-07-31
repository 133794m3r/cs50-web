from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods
from json import loads as json_decode
from json import dumps as json_encode

from .models import User,Challenges,Solves,Hints,Files
from .util import *


# Create your views here.
def profile(request,username):
	pass

def index(request):
	challenges= Challenges.objects.all()
	chals,categories = make_index(challenges)
	return render(request,"index.html",{'challenges':chals,'categories':categories})


def login_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request,"login.html",{
				"message":"Invalid username and/or password."
			})
	else:
		return render(request,"login.html")


@login_required(login_url='login')
@require_http_methods(["GET"])
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


@require_http_methods(["GET"])
def chal(request,challenge):
	pass

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		#email = request.POST["email"]

		password=request.POST["password"]
		confirmation=request.POST["password_confirm"]

		if password != confirmation:
			return render(request,"register.html",{
				"message":"Passwords must match."
			})
		elif len(password) < 5:
			return render(request,"register.html",{
				"message":"Password must be the minimum strength."
			})

		try:
			user = User.objects.create_user(username,email,password)
			user.save()
		except IntegrityError:
			return render(request,"register.html",{
				"message":"Username must be unique."
			})
		login_view(request,user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request,"register.html")


@login_required(login_url='login')
@require_http_methods(["POST"])
def solve(request,chal):
	pass

@login_required(login_url='login')
@require_http_methods(["POST"])
def hint(request,hint_id):
	pass

@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def control_panel(request,username):
	pass

def solves(request):
	pass

@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def challenge_admin(request):
	if request.method == "POST":
		content = json_decode(request.body)
	else:

		return render(request,"challenge_admin.html",{"challenges":CHALLENGES,'json':json_encode(CHALLENGES)})
