from django.contrib import admin

# Register your models here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from ratelimit.decorators import ratelimit


class RateLimitedAdmin(admin.AdminSite):

	@method_decorator(never_cache)
	@method_decorator(ratelimit(key='ip',rate='3/m',method=ratelimit.UNSAFE,block=True))
	@method_decorator(ratelimit(key='post:username',rate='3/m',method=ratelimit.UNSAFE,block=True))
	def login(self,request,extra_context=None):
		return super(RateLimitedAdmin,self).login(request,extra_context)

