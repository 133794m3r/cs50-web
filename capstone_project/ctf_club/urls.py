from django.urls import path
from . import views
urlpatterns = [
	path("profile/<str:username>",views.profile,name="profile"),
	path("register",views.register,name="register"),
	path("",views.index,name="index"),
	path("login",views.login_view,name="login"),
	path("logout",views.logout_view,name="logout"),
	path("challenge/<int:challenge_id>",views.challenge_view,name="challenge_view"),
	path("solve/<int:challenge_id>",views.solve,name="solve"),
	path("solves",views.solves,name="solved_challenges"),
	path("hint/<int:id>",views.hint,name="hint"),
	path("control_panel/<str:username>",views.control_panel,name="control_panel"),
	path("challenge_admin",views.challenge_admin,name="challenge_admin")
]