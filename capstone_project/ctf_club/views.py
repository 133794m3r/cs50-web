from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse,HttpResponseNotFound,Http404
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods
from json import loads as json_decode
from json import dumps as json_encode
from django.contrib.auth.forms import PasswordChangeForm

"""
CTFClub Project
By Macarthur Inbody <admin-contact@transcendental.us>
Licensed AGPLv3 Or later (2020)
"""

from .models import *
from .util import *


# Create your views here.
@require_http_methods(["GET","POST"])
def profile(request,username):
	return render(request,'control_panel.html')


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

	solved = False if Solves.objects.filter(user_id=request.user.id,challenge_id=challenge_id).count() == 0 else True

	#If they've already solved it might as well show them the flag.
	if solved:
		chal = Challenges.objects.values('id','name','description','points','flag').get(id=challenge_id)
	else:
		chal = Challenges.objects.values('id', 'name', 'description', 'points').get(id=challenge_id)


	hints = Hints.objects.filter(challenge_id=chal['id']).values('id','level')
	num_hints = hints.count()


	print(hints)
	chal = jsonify_queryset(chal)
	hints = jsonify_queryset(hints)
	resp = {'challenge': chal, 'hints': hints,'num_hints':num_hints,'solved':solved}
	return JsonResponse(resp)

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
			login(request,user)			
		except IntegrityError:
			return render(request,"register.html",{
				"message":"Username must be unique."
			})

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
	print(answer)
	solved = Solves.objects.filter(user=request.user,challenge_id=challenge_id).first()
	print(correct_flag == answer)
	print(correct_flag)
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
	unlocked = HintsUnlocked.objects.filter(hint_id=hint_id,user_id=request.user.id)

	if unlocked.count() == 0:
		hint_unlock = HintsUnlocked.objects.create(hint_id=hint_id,user_id=request.user.id)
#		hint_unlock.save()
		print(unlocked)
	else:
		pass
	print(unlocked)
	#give them just the hint itself as part of the result.
	revealed_hint = jsonify_queryset(Hints.objects.filter(id=hint_id).values('description'))
	print(revealed_hint)
	return JsonResponse(revealed_hint)


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def control_panel(request,username):
	form = PasswordChangeForm(request.user)
	if request.user.is_authenticated:
		if request.method == "POST":
			content = json_decode(request.body)
			old_password=content['old_password']
			new_password=content['new_password']
			confirm_password=content['confirm_password']
			print(content)
			if old_password == '' or new_password == '':
				msg = "Passwords can't be blank."
			elif old_password != new_password and new_password == confirm_password:
				if request.user.check_password(old_password):
					request.user.set_password(new_password)
					request.user.save()
					update_session_auth_hash(request,request.user)
					msg = "Password updated successfully."
				else:
					msg = "Password does not match your old password."
			elif old_password == new_password:
				msg = "New password is the same as the old password."
			elif new_password != confirm_password:
				msg = "New passwords must match."

			return JsonResponse({'ok':True,'msg':msg})

	return render(request,'control_panel.html',{'form':form})


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
	return render(request,"solves.html",{"objects":all_solves,'num_solves':num_solves})


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def challenge_admin(request):
	#If the user is not an admin or in the staff pretend like this route doesn't exist.
	if not request.user.is_staff or not request.user.is_superuser:
		#return HttpResponseNotFound("<h1>Error 404</h1><h2> That route doesn't exist on this server.</h2>")
		raise Http404()
	print(request.method)
	if request.method == "POST":
		print('posted')
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
			print('edited')
		else:
			print('else')
			print(name,description,flag,points,category)
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
		base_challenges = []
		varieties_used = {}
		variety = None
		for challenge in challenges:

			#Remove the - {VARIETY} part.
			tmp_name = ''
			#This is a hack until I modify the model to incldue the "variety" flag.
			if '-' in challenge.name and challenge.name[-1].isdigit():
				tmp_name = challenge.name[:-4]
				variety = challenge.name[-1]
			else:
				tmp_name = challenge.name
				variety = None
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
					challenges_used.append(indexed)
					all_challenges.append({
						'name':tmp_name, 'category':challenge.category.name, 'full_description':challenge.description,
						'description':challenge_template['description'], 'sn':challenge_template['sn'],
						'edit':True, 'flag':challenge.flag})
					base_challenges.append({
						'name':tmp_name, 'category':challenge.category.name, 'full_description':challenge.description,
						'description':challenge_template['description'], 'sn':challenge_template['sn'],
						'edit':True, 'flag':challenge.flag})


		for i,challenge in enumerate(CHALLENGES_TEMPLATES):
			if challenge['variety']:
				if i in challenges_used:
					if varieties_used.get(i):
					#	print(varieties_used)
						if len(varieties_used[i]) == 2:
							challenge['edit'] = True
					base_challenges.append(challenge)
					all_challenges.append(challenge)
				else:
					challenge['edit'] = False
					all_challenges.append(challenge)
			elif i not in challenges_used:
				base_challenges.append(challenge)
				all_challenges.append(challenge)

		return render(request,"challenge_admin.html", {"challenges":base_challenges,
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
@require_http_methods(["POST","GET"])
def hint_admin(request,challenge_name):
	if request.method == "POST":
		content = json_decode(request.body)
		print(content)
		if content['id'] == 0:
			new_hint = Hints.objects.create(
				description=content['description'],
				level=content['level'],
				challenge_id = Challenges.objects.get(name=challenge_name).id
			)
		else:
			edit_hint = Hints.objects.get(pk=content['id'])
			edit_hint.description = content['description']
			edit_hint.level = content['level']
			print(edit_hint)
			edit_hint.save()

		return JsonResponse({'OK':True})
	else:
		print(challenge_name)
		challenge_hints = Hints.objects.filter(challenge__name=challenge_name)
		num_hints = challenge_hints.count()
		challenge_hints = jsonify_queryset(challenge_hints)
		print(challenge_hints)
	return JsonResponse({'hints':challenge_hints,'len':num_hints})

@login_required()
def admin_view(request):
	return render(request,"solves_admin.html",{'solves:solves'})
