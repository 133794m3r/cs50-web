from django.urls import path,re_path
from . import views
"""
CTFClub Project
By Macarthur Inbody <admin-contact@transcendental.us>
Licensed AGPLv3 Or later (2020)
"""
urlpatterns = [
	# path("profile/<str:username>",views.profile,name="profile"),
	path("register",views.register,name="register"),
	path("",views.index,name="index"),
	path("login",views.login_view,name="login"),
	path("logout",views.logout_view,name="logout"),
	path("challenge/<int:challenge_id>",views.challenge_view,name="challenge_view"),
	path("solve/<int:challenge_id>",views.solve,name="solve"),
	path("solves",views.solves,name="solved_challenges"),
	path("solves/<str:username>",views.solves,name="solved_challenges"),
	path("hint/<int:hint_id>",views.hint,name="hint"),
	path("control_panel/<str:username>",views.control_panel,name="control_panel"),
	path("admin/challenge",views.challenge_admin,name="challenge_admin"),
	re_path(r"^admin/challenge/hints/(?P<challenge_name>.+?)/$",views.hint_admin,name="admin_hint"),
	path("admin/solves", views.solves_admin, name="solves_admin"),
	path("admin/",views.admin_view,name="admin"),
	path("highscores/",views.high_scores,name="high_scores"),
	path("captcha/",views.captcha,name="captcha"),
	re_path(r"^file/(?P<filename>[A-Za-z\-_0-9.]+)$",views.file,name="file"),
	path("tfa_qrcode.png",views.tfa_qr_code,name="tfa_qrcode"),
	path("two_factor",views.tfa_enable,name="two_factor"),
	path("verify_tfa",views.verify_tfa,name="verify_tfa"),
	path("about",views.about,name="about"),

	path("leaderboard",views.leaderboard,name="leaderboard"),
]