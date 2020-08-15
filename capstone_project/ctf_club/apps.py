from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class CtfClubConfig(AppConfig):
	name = 'ctf_club'

class RateLimitedAdminConfig(AdminConfig):
	default_site = 'ctf_club.admin.RateLimitedAdmin'