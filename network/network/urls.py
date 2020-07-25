
from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("new_post",views.new_post, name="new_post"),
	path("profile/<str:username>",views.profile,name="profile"),
	path("edit/<int:post_id>",views.edit,name="edit"),
	path("follow/<int:id>",views.follow,name="follow"),
	path("like/<int:post_id>",views.like,name="like"),
	path("following",views.home,name="following"),
	path("edit/post/<int:post_id>",views.edit_post,name="edit_post")
]
