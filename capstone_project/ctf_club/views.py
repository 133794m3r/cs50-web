from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse,HttpResponseNotFound,Http404
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
	challenges=Challenges.objects.all()
	chals= make_index(challenges)
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
	return JsonResponse(chal.to_dict())

def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('index')

	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")

		password=request.POST.get("password")
		confirmation=request.POST.get("password_confirm")

		if password != confirmation:
			return render(request,"register.html",{
				"message":"Passwords must match."
			})
		elif password is None:
			return render(request,"register.html",{
				"message":"Password cannot be blank."
			})
		elif username is None:
			return render(request,"register.html",{
				"message":"Username can't be blank."
			})
		elif len(password) < 5:
			return render(request,"register.html",{
				"message":"Password must be the minimum strength."
			})

		try:
			user = User.objects.create_user(username=username,email=email,password=password)
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

	challenge = Challenges.objects.filter(pk=challenge_id).first()
	data = json_decode(request.body)

	#Make sure that all matches are case-insensitve for simplicty's sake.
	answer = data['answer'].upper()
	correct_flag = challenge.flag.upper()

	solved = Solves.objects.filter(user=request.user,challenge_id=challenge_id).first()

	#if they have solved something don't do anything else.
	if solved:
		was_solved = True
	#they hadn't already solved it see if they did solve it.
	elif answer == correct_flag:
		#if so make sure to create a new solve.
		new_solve = Solves.objects.create(
			user=request.user,
			challenge_id=challenge_id
		)
		new_solve.save()
		#modify the number of solves to increase it by one.
		challenge.num_solves +=1
		challenge.save()
		was_solved = True
	#otherwise no solve was had.
	else:
		was_solved = False

	return JsonResponse({'solved':was_solved})


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def challenge_hint(request,challenge_id):
	pass

@login_required()
@require_http_methods(["GET","POST"])
def hint(request,hint_id):
	pass

@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def control_panel(request,username):
	pass


@login_required(login_url='login')
def solves(request):
	all_solves = {}
	num_solves = 0
	user_solves = Solves.objects.filter(user=request.user)
	if user_solves.first() is None:
		all_solves = {}
		num_solves = 0
	else:
		all_solves = jsonify_queryset(user_solves.all())
		num_solves = user_solves.count()

	print(all_solves)
	#return JsonResponse(all_solves)
	return render(request,"solves.html",{"objects":all_solves,'num_solves':num_solves})


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def challenge_admin(request):
	#If the user is not an admin or in the staff pretend like this route doesn't exist.
	if not request.user.is_staff or not request.user.is_superuser:
		#return HttpResponseNotFound("<h1>Error 404</h1><h2> That route doesn't exist on this server.</h2>")
		raise Http404()

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
				#if content.get('edit'):
				name +=f' - {variety}'
				description,flag = CHALLENGE_FUNCS[content['sn']](plaintext,variety)
			else:
				description,flag = CHALLENGE_FUNCS[content['sn']](plaintext)
		points = content.get('points') or 100
		if content.get('edit'):
			challenge = Challenges.objects.get(name=name)
			challenge.description = description
			challenge.flag = flag
			challenge.num_solves = 0
			challenge.save()
			#remove all solves for the challenge as it's been modified.
			Solves.objects.filter(challenge_id=challenge.id).delete()
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
				#	print(varieties_used)
					if len(varieties_used[i]) == 2:
						challenge['edit'] = True


				all_challenges.append(challenge)
			else:
				challenge['edit'] = False
				all_challenges.append(challenge)

		return render(request,"challenge_admin.html", {"challenges":all_challenges,
		                                               'json':json_encode(all_challenges)})


@login_required()
def solves_admin(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404()
	all_challenges = Challenges.objects.order_by('category__name').values('id','name','category__name','num_solves')
	all_challenges = jsonify_queryset(all_challenges)

	#return JsonResponse(all_challenges,safe=False)
	return render(request,"solves_admin.html",{"challenges":all_challenges})


@login_required()
def get_all_solves(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404()

	all_solves = Solves.objects.order_by('challenge__category__name').values('user__username', 'challenge__name', 'challenge__category__name', 'timestamp')
	all_solves = jsonify_queryset(all_solves)
	solve_dict = {}

	if type(all_solves) is dict:
		solve_dict[all_solves.get('challenge__category__name')] = [all_solves]
	elif len(all_solves) > 1:
		for isolve in all_solves:
			if solve_dict.get(isolve['challenge__category__name']):
				solve_dict[isolve['challenge__category__name']].append(isolve)
			else:
				solve_dict[isolve['challenge__category__name']] = [isolve]
	else:
		pass

	return JsonResponse({'error':solve_dict})


@login_required()
def admin_view(request):
	return render(request,"solves_admin.html",{'solves:solves'})