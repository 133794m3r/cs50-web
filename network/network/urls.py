
from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("new_post",views.new_post, name="new_post"),
	path("<str:username>",views.user,name="user"),
	path("edit/<int:post_id>",views.edit,name="edit"),
	path("follow/<int:id>",views.follow,name="follow")
]
