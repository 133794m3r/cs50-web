from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from datetime import datetime
from .models import User,Post

def index(request):
	posts = list(reversed(Post.objects.all()))
	paginator = Paginator(posts,10)
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)
	return render(request, "network/index.html",{'page_obj':page,'iterator':paginator.page_range})


def login_view(request):

	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "network/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "network/login.html")


def logout_view(request):

	logout(request)
	return HttpResponseRedirect(reverse("index"))


def register(request):

	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "network/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "network/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "network/register.html")

@login_required(login_url='login')
def like(request,post_id):
	post = Post.objects.get(pk=post_id)
	liked = false
	if request.user in post.likes.all():
		post.likes.remove(request.user)
	else:
		post.likes.add(request.user)
		liked = true

	likes = post.likes.count()

	return JSONResponse({
		'liked':liked,
		'likes':likes
	})

@login_required(login_url='login')
@require_http_methods(["POST"])
def new_post(request):
	Post.objects.create(
		username = request.user,
		content = request.POST['content'],
		datetime = datetime.now()
	)

	return HttpResponseRedirect(reverse('index'))

def user(request,username):
	user_chosen = User.objects.get(username=username)

	posts= list(reversed(user_chosen.posts.all()))
	paginator = Paginator(posts,10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,"network/user.html",{'selected_user':user_chosen,'page_obj':page_obj,'pages':paginator.page_range})

def edit(request,post_id):
	pass

@login_required(login_url='login')
@require_http_methods(["POST"])
def follow(request,user_id):
	pass

@login_required(login_url='login')
@require_http_methods(["POST"])
def following_posts(request):
	pass