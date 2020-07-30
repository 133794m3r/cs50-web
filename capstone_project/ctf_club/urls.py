from django.urls import path
from . import views
urlpatterns = [
	path("profile/<str:username>",views.profile,name="profile"),
	path("register",views.register,name="register"),
	path("",views.index,name="index"),
	path("login",views.login,name="login"),
	path("logout",views.logout,name="logout"),
	path("chal/<int:id>",views.chal,name="challenge"),
	path("solve/<int:id>",views.solve,name="solve"),
	path("solves",views.solves,name="solved_challenges"),
	path("hint/<int:id>",views.hint,name="hint"),
	path("control_panel/<str:username>",views.control_panel,name="control_panel"),
	path("challenge_admin",views.challenge_admin,name="challenge_admin")
]