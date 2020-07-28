from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	followers = models.ManyToManyField('self',symmetrical=False,related_name='following')

class Post(models.Model):
	username = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
	content = models.TextField()
	datetime = models.DateTimeField()
	likes = models.ManyToManyField(User)
