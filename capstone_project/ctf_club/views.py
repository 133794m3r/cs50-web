from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods

from .models import User,Challenges,Solves,Hints,Files
from json import loads as json_decode

# Create your views here.
def profile(request,username):
	pass

def index(request):
	challenges= Challenges.objects.all()
	return render(request,"index.html")

def login(request):
	pass

@login_required(login_url='login')
def logout(request):
	pass

@require_http_methods(["GET"])
def chal(request,challenge):
	pass

def register(request):
	pass

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