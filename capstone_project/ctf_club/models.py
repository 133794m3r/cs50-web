from django.db import models
from django.contrib.auth.models import AbstractUser

# User model is just here so I can reference it, I use the default model.
class User(AbstractUser):
	pass


class Categories(models.Model):
	name = models.CharField(max_length=50)


class Challenges(models.Model):
	category = models.ForeignKey('Categories',on_delete=models.CASCADE,related_name='category')
	points = models.IntegerField()
	name = models.CharField(max_length=50)
	description = models.TextField()
	flag = models.TextField()


class Solves(models.Model):
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='solves')
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='solves')


class Files(models.Model):
	filename = models.TextField()
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='files')


class Hints(models.Model):
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='hints')
	description = models.TextField()
	hidden = models.BooleanField(default=True)
	level = models.IntegerField()
	used = models.ManyToManyField(User)