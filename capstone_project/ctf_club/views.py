#all of the django specific stuff.
from django.db import IntegrityError
from django.shortcuts import  render
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse,HttpResponseNotFound,Http404,FileResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods

#JSON items.
from json import loads as json_decode
from json import dumps as json_encode

#ratelimiter
from ratelimit.decorators import ratelimit
"""
CTFClub Project
By Macarthur Inbody <admin-contact@transcendental.us>
Licensed AGPLv3 Or later (2020)
"""

from .models import *
from .util import *

def is_ratelimited(request):
	return getattr(request,'limited',False)

# Create your views here.
@require_http_methods(["GET","POST"])
@ratelimit(key='ip',rate='20/m')
def profile(request,username):
	return render(request,'control_panel.html')

@ratelimit(key='ip',rate='1/s')
def index(request):
	challenges=Challenges.objects.all()
	chals= make_index(challenges)
	return render(request,"index.html",{'objects':chals})

@require_http_methods(["GET","POST"])
@ratelimit(key='ip',rate='30/m',method=ratelimit.UNSAFE)
@ratelimit(key='post:username',rate='5/m',method=ratelimit.UNSAFE)
def login_view(request):
	if is_ratelimited(request):
		request.session['require_captcha'] = True
		request.session['captcha_valid'] = False
	else:
		request.session['require_captcha'] = False

	show_captcha = False
	captcha_msg = ''

	if request.session.get('require_captcha',False) and not request.session.get('captcha_valid',False):
		captcha_msg,ans = simple_math()
		show_captcha = True
		old_ans = request.session.get('captcha_answer')
		if old_ans is None:
			old_ans = ans
		request.session['captcha_answer'] = ans

	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]

		#if they're rate-limited send this message.
		if is_ratelimited(request):
			print(show_captcha)
			print(captcha_msg)
			return render(request,"login.html",{
				"message":"You're trying to fast please slow down.",
				"show_captcha":show_captcha,
				"captcha_msg":captcha_msg
			})

		#if the captcha is wrong then don't even bother trying to auth them.
		if request.session.get('require_captcha',False):
			if not request.session.get('captcha_valid',False):
				if request.POST.get('captcha_ans') != old_ans:
					return render(request,"login.html",{
						"message":"Incorrect Captcha",
						"show_captcha":show_captcha,
						"captcha_msg":captcha_msg
					})

		user = authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request,"login.html",{
				"message":"Invalid username and/or password.",
				"show_captcha":show_captcha,
				"captcha_msg":captcha_msg
			})
	else:
		return render(request,"login.html")


@login_required(login_url='login')
@require_http_methods(["GET"])
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


@require_http_methods(["GET"])
@login_required(login_url='login')
@ratelimit(key='user',rate='45/m')
def challenge_view(request,challenge_id):

	solved = False if Solves.objects.filter(user_id=request.user.id,challenge_id=challenge_id).count() == 0 else True

	#If they've already solved it might as well show them the flag.
	if solved:
		chal = Challenges.objects.values('id','name','description','points','flag').get(id=challenge_id)
	else:
		chal = Challenges.objects.values('id', 'name', 'description', 'points').get(id=challenge_id)


	hints = Hints.objects.filter(challenge_id=chal['id']).values('id','level')
	num_hints = hints.count()

	chal = jsonify_queryset(chal)
	hints = jsonify_queryset(hints)
	resp = {'challenge': chal, 'hints': hints,'num_hints':num_hints,'solved':solved}
	return JsonResponse(resp)
	
@require_http_methods(["GET","POST"])
@ratelimit(key='ip',rate='60/m',method=ratelimit.UNSAFE)
def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('index')
	captcha_msg,ans = simple_math()

	if request.method == "POST":
		msg = ''
		if getattr(request,'limited',False):
			return render(request,"register.html",{"message":"You're going too fast. Slow down.","captcha_msg":captcha_msg})

		username = request.POST.get("username")
		email = request.POST.get("email")

		password=request.POST.get("password")
		confirmation=request.POST.get("password_confirm")
		given_ans = request.POST.get("captcha_ans")
		old_ans = request.session['captcha_answer']
		request.session['captcha_answer'] = ans
		if not request.session['captcha_valid']:
			if given_ans != request.session['answer']:
				return render(request,"register.html",{
					"message":"Invalid Captcha Answer.",
					"captcha_msg":captcha_msg
				})
		else:
			request.session['captcha_valid'] = False


		if password != confirmation:
			return render(request,"register.html",{
				"message":"Passwords must match.",
				"captcha_msg":captcha_msg
			})
		elif password is None:
			return render(request,"register.html",{
				"message":msg + "Password cannot be blank.",
				          "captcha_msg":captcha_msg
			})
		elif username is None:
			return render(request,"register.html",{
				"message":"Username can't be blank.",
				"captcha_msg": captcha_msg
			})
		elif len(password) < 5:
			return render(request,"register.html",{
				"message":"Password must be the minimum strength.",
				"captcha_msg": captcha_msg
			})

		try:
			user = User.objects.create_user(username=username,email=email,password=password)
			user.save()
			login(request,user)			
		except IntegrityError:
			return render(request,"register.html",{
				"message":"Username must be unique.",
				"captcha_msg": captcha_msg
			})
		request.session['captcha_valid'] = False
		return HttpResponseRedirect(reverse("index"))
	else:
		request.session['captcha_answer'] = ans
		return render(request,"register.html",{"captcha_msg":captcha_msg})


@login_required(login_url='login')
@require_http_methods(["POST"])
@ratelimit(key='user',rate='20/m')
def solve(request,challenge_id):

	challenge = Challenges.objects.filter(pk=challenge_id).first()
	data = json_decode(request.body)

	#Make sure that all matches are case-insensitve for simplicty's sake.
	answer = data['answer'].upper()
	correct_flag = challenge.flag.upper()
	points = challenge.points
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
		#Really really stupid way to do an update statement here. But MVC is the future they say.
		# would be so much simpler to simply do an sql query like.
		# update ctf_club_user set points = points + challenge_points where id = user_id
		#One clean line of SQL instead of 3 lines of nonsense.
		user = User.objects.get(pk=request.user.id)
		user.points+=points
		user.save()
	#otherwise no solve was had.
	else:
		was_solved = False

	return JsonResponse({'solved':was_solved})


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
def challenge_hint(request,challenge_id):
	pass

@login_required(login_url='login')
@ratelimit(key='user',rate='20/m')
@require_http_methods(["GET","POST"])
def hint(request,hint_id):
	unlocked = HintsUnlocked.objects.filter(hint_id=hint_id,user_id=request.user.id)

	if unlocked.count() == 0:
		hint_unlock = HintsUnlocked.objects.create(hint_id=hint_id,user_id=request.user.id)

	else:
		pass
	#give them just the hint itself as part of the result.
	revealed_hint = jsonify_queryset(Hints.objects.filter(id=hint_id).values('description'))

	return JsonResponse(revealed_hint)


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
@ratelimit(key='user',rate='20/m',method=ratelimit.UNSAFE)
def control_panel(request,username):

	if request.user.is_authenticated:
		if request.method == "POST":
			content = json_decode(request.body)
			old_password=content['old_password']
			new_password=content['new_password']
			confirm_password=content['confirm_password']
			if is_ratelimited(request):
				msg = "You're submitting too fast."
			elif old_password == '' or new_password == '':
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
	points = User.objects.get(username=username).points

	return render(request,'control_panel.html',{'points':points,'username':username})

@ratelimit(key='user',rate='30/m')
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

	return render(request,"solves.html",{"objects":all_solves,'num_solves':num_solves})


@login_required(login_url='login')
@require_http_methods(["GET","POST"])
@ratelimit(key='user',rate='10/s')
def challenge_admin(request):
	#for the sorting of the challenges later.
	from operator import itemgetter
	#If the user is not an admin or in the staff pretend like this route doesn't exist.
	if not request.user.is_staff or not request.user.is_superuser:
		#return HttpResponseNotFound("<h1>Error 404</h1><h2> That route doesn't exist on this server.</h2>")
		raise Http404()

	if request.method == "POST":
		file = None
		description = ''
		flag = ''
		content = json_decode(request.body)
		print(content);
		name = content['name']
		category = content['category']
		if content['sn'] == 'fizzbuzz':
			min = content['min']
			max = content['max']
			description,flag = CHALLENGE_FUNCS[content['sn']](min,max)
		elif content['sn'] == 'master_hacker':
			description,flag, file = CHALLENGE_FUNCS[content['sn']]()
		else:
			plaintext = content['plaintext']
			if content['sn'] in ["affine","hill"]:
				variety = content['variety']
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
			#remove all solves for the challenge as it's been modified
			old_solves = Solves.objects.filter(challenge_id=challenge.id)
			for user_solve in old_solves:
				User.objects.filter(pk=user_solve.user_id).update(points=0)
			#delete the old solves finally.
			old_solves.delete()

		else:
			print(category)
			challenge = Challenges.objects.create(
				name = name,
				description = description,
				flag = flag,
				points = points,
				category = Categories.objects.get(name=category)
			)
			if file is not None:
				file_obj = Files.objects.create(
					filename=file
				)
				challenge.files.add(file_obj)
		print({'description':description,'flag':flag,'file':file})
		return JsonResponse({'description':description,'flag':flag,'file':file})
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
				variety = int(challenge.name[-1])
			else:
				tmp_name = challenge.name
				variety = None

			if tmp_name in CHALLENGES_TEMPLATES_NAMES:
				indexed = CHALLENGES_TEMPLATES_NAMES[tmp_name][1]
				challenges_used.append(indexed)
				challenge_template = CHALLENGES_TEMPLATES[indexed]
				chal_obj = {
					'name': tmp_name, 'category': challenge.category.name, 'full_description': challenge.description,
					'description': challenge_template['description'], 'sn': challenge_template['sn'],
					'edit': True, 'flag': challenge.flag, 'can_have_files':challenge_template['files']}
				if variety is not None:
					if varieties_used.get(indexed):
						varieties_used[indexed].append(variety)
					else:
						varieties_used[indexed]=[variety]
					chal_obj['variety'] = variety
					all_challenges.append(chal_obj)
				else:
					challenges_used.append(indexed)
					base_challenges.append(chal_obj)
					if challenge_template['files']:
						print(challenge.files.all())
						files = challenge.files.all()
						chal_obj['files'] = [jsonify_queryset(files)] if files.count() == 1 else jsonify_queryset(files)
					all_challenges.append(chal_obj)
				challenges_used.append(indexed)


		for i,challenge in enumerate(CHALLENGES_TEMPLATES):
			if challenge['variety']:
				if i in challenges_used:
					if varieties_used.get(i):
						if len(varieties_used[i]) == 2:
							challenge['edit'] = True
					base_challenges.append(challenge)
					all_challenges.append(challenge)
				else:
					challenge['edit'] = False
					base_challenges.append(challenge)
					all_challenges.append(challenge)
			elif i not in challenges_used:
				base_challenges.append(challenge)
				all_challenges.append(challenge)
		new_chals = sorted(base_challenges,key=itemgetter('category','sn','name'))
		return render(request,"challenge_admin.html", {"challenges":new_chals,
		                                               'json':json_encode(all_challenges)})


@login_required(login_url='login')
@ratelimit(key='user',rate='45/m')
def solves_admin(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404()
	all_challenges = Challenges.objects.order_by('category__name').values('id','name','category__name','num_solves')
	all_challenges = jsonify_queryset(all_challenges)
	#return JsonResponse(all_challenges,safe=False)
	return render(request,"solves_admin.html",{"challenges":all_challenges})


@login_required(login_url='login')
@ratelimit(key='user',rate='30/m')
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

@login_required(login_url='login')
@ratelimit(key='user',rate='1/s')
@require_http_methods(["POST","GET"])
def hint_admin(request,challenge_name):
	if request.method == "POST":
		content = json_decode(request.body)
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
			edit_hint.save()

		return JsonResponse({'OK':True})
	else:
		challenge_hints = Hints.objects.filter(challenge__name=challenge_name)
		num_hints = challenge_hints.count()
		challenge_hints = jsonify_queryset(challenge_hints)
	return JsonResponse({'hints':challenge_hints,'len':num_hints})

@login_required(login_url='login')
@ratelimit(key='ip',rate='30/m')
def admin_view(request):
	if request.user.is_staff != True or request.user.is_superuser != True:
		raise Http404()

	was_limited = getattr(request, 'limited', False)
	return render(request,"solves_admin.html",{'solves:solves'})

@ratelimit(key='ip',rate='30/m')
@require_http_methods(["GET"])
def high_scores(request):
	top_users = User.objects.values('points','username','id').order_by('-points','username')[:10]
	was_limited = getattr(request, 'limited', False)
	return JsonResponse(jsonify_queryset(top_users),safe=False)

@ratelimit(key='ip',rate='1/s',method=ratelimit.UNSAFE)
@require_http_methods(["GET","POST"])
def captcha(request):
	if request.method == "POST":
		if request.is_ajax():
			usr_ans = json_decode(request.body)['captcha_ans']
		else:
			usr_ans = request.POST.get('captcha_ans')

		if usr_ans == request.session['captcha_answer']:
			request.session['captcha_valid'] = True
			msg = "Captcha Solved";
			error = False
		else:
			request.session['captcha_valid'] = False
			msg = "Invalid Captcha Answer."
			error = True
	else:
		request.session['captcha_valid'] = False
	captcha_msg,ans = simple_math()
	request.session['captcha_answer'] = ans
	return JsonResponse({"msg":msg,"error":error,"captcha_msg":captcha_msg})

@login_required(login_url='login')
def files(request,filename):
	return FileResponse(open(f'files/{filename}','rb'))