from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods
from json import loads as json_decode
from json import dumps as json_encode

from .models import User,Challenges,Solves,Hints,Files,Categories
from .util import *


# Create your views here.
def profile(request,username):
	pass

def index(request):
	challenges= Challenges.objects.all()
	chals= make_index(challenges)
	print(chals)

	return render(request,"index.html",{'objects':chals})


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
def challenge_view(request,challenge_id):
	chal = Challenges.objects.get(pk=challenge_id)
	print(chal)
	return JsonResponse({'content':None})
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
			user = User.objects.create_user(username=username,password=password)
			user.save()
		except IntegrityError:
			return render(request,"register.html",{
				"message":"Username must be unique."
			})
		login(request,user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request,"register.html")


@login_required(login_url='login')
@require_http_methods(["POST"])
def solve(request,challenge_id):
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
		description = ''
		flag = ''
		content = json_decode(request.body)
		print(content)
		name = content['name']
		category = content['category']
		if content['sn'] == 'fizzbuzz':
			min = content['min']
			max = content['max']
			description,flag = CHALLENGE_FUNCS[content['sn']](min,max)
		else:
			plaintext = content['plaintext']
			if content['sn'] in ["affine","hill"]:
				variety = content['variety']
				if content.get('edit'):
					name +=f' - {variety}'
				description,flag = CHALLENGE_FUNCS[content['sn']](plaintext,variety)
			else:
				description,flag = CHALLENGE_FUNCS[content['sn']](plaintext)
		points = content.get('points') or 100
		if content.get('edit'):
			print(name)
			challenge = Challenges.objects.get(name=name)
			challenge.description = description
			challenge.flag = flag
			challenge.save()
		else:
			Challenges.objects.create(
				name = name,
				description = description,
				flag = flag,
				points = points,
				category = Categories.objects.get(name=category)
			)

		return JsonResponse({'description':description,'flag':flag})
	else:
		challenges = Challenges.objects.all()
		all_challenges = []
		challenges_used = []
		varieties_used = {}
		variety = None
		for challenge in challenges:
			#Remove the - {VARIETY} part.
			tmp_name = ''
			if '-' in challenge.name:
				tmp_name = challenge.name[:-4]
				variety = challenge.name[-1]
			else:
				tmp_name = challenge.name
			print(tmp_name)
			if tmp_name in CHALLENGES_TEMPLATES_NAMES:
				indexed = CHALLENGES_TEMPLATES_NAMES[tmp_name][1]
				challenges_used.append(indexed)
				challenge_template = CHALLENGES_TEMPLATES[indexed]
				if variety:
					if varieties_used.get(indexed):
						varieties_used[indexed].append(variety)
					else:
						varieties_used[indexed]=[variety]
					all_challenges.append({
						'name':challenge.name, 'category':challenge.category.name, 'full_description':challenge.description,
						'description':challenge_template['description'], 'sn':challenge_template['sn'], 'variety':variety,
						'edit':True, 'flag':challenge.flag})
				else:

					all_challenges.append({
						'name':tmp_name, 'category':challenge.category.name, 'full_description':challenge.description,
						'description':challenge_template['description'], 'sn':challenge_template['sn'],
						'edit':True, 'flag':challenge.flag})

		for i,challenge in enumerate(CHALLENGES_TEMPLATES):
			if i in challenges_used:
				if varieties_used.get(i):
						if len(varieties_used[i]) != 2:
							all_challenges.append(challenge)
				else:
					continue
			else:
				challenge['edit'] = False
				all_challenges.append(challenge)

		return render(request,"challenge_admin.html", {"challenges":all_challenges,
		                                               'json':json_encode(all_challenges)})
