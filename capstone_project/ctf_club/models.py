from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

"""
CTFClub Project
By Macarthur Inbody <admin-contact@transcendental.us>
Licensed AGPLv3 Or later (2020)
"""

# User model is just here so I can reference it, I use the default model.
class User(AbstractUser):
	points = models.IntegerField(default=0)
	def to_dict(self):
		return {'id':self.id, 'username':self.username, 'email':self.email,
		        'is_staff':self.is_staff, 'is_superuser':self.is_superuser,
		        'first_name':self.first_name, 'last_name':self.last_name,
		        'date_joined':self.date_joined, 'is_active':self.is_active,
		        'last_login':self.last_login
		}


class Categories(models.Model):
	name = models.CharField(max_length=50)

	def to_dict(self):
		return {'id':self.id,'name':self.name}

	def __repr__(self):
		return 'Categories(name={!r},id={!r})'.format(self.name,self.id)

	def __str__(self):
		return self.__repr__()

	def __len__(self):
		return 1

class Challenges(models.Model):
	category = models.ForeignKey('Categories',on_delete=models.CASCADE,related_name='category')
	points = models.IntegerField()
	name = models.CharField(max_length=50)
	description = models.TextField()
	flag = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now)
	num_solves = models.IntegerField(default=0)

	def __repr__(self):
		return 'Challenges(id={!r},category={!r},points={!r},name={!r},description={!r},flag={!r},timestamp={!r},num_solves={!r}'.format(self.id,self.category,self.points,self.name,self.description,self.flag,self.timestamp,self.num_solves)

	def __str__(self):
		return self.__repr__()

	def to_dict(self):
		"""
		to_dict method returns a dict representation of the object.

		:return: {dict} A dict containing the fields that are important.
		"""
		return {'id':self.id,'category':self.category.name,'name':self.name,'points':self.points,'description':self.description,'flag':self.flag,'timestamp':self.timestamp,'num_solves':self.num_solves}

	def __len__(self):
		return 1

class Solves(models.Model):
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='solves')
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='solves')
	timestamp = models.DateTimeField(default=timezone.now)

	def to_dict(self):
		__chal = self.challenge.to_dict()
		__user = self.user.to_dict()
		return {'challenge_id':__chal['id'],'challenge_name':__chal['name'],'challenge_category':__chal['category'],'challenge_flag':__chal['flag'],'username':__user['username']}


	def __repr__(self):
		return 'Solves(challenge={!r},user={!r},timestamp={!r})'.format(self.challenge,self.user,self.timestamp)


	def __str__(self):
		return self.__repr__()


	def __len__(self):
		return 1


# Was going to make this it's own table but honestly why. It's a single field and should be part of the challenge itself.
# this way it can be easily removed.
# class TotalSolves(models.Model):
# 	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE)
# 	num_solves = models.IntegerField()
#
# 	def to_dict(self):
# 		return {'id':self.id,'challenge_id':self.challenge_id,'challenge_name':self.challenge.name,'category_name':self.challenge.category.name,'category_id':self.challenge.category.id}
#
# 	def __repr__(self):
# 		return 'TotalSolves(challenge={!r},num_solves={!r}'.format(self.challenge,self.num_solves)

class Files(models.Model):
	filename = models.TextField()
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='files')

	def __len__(self):
		return 1

	def __repr__(self):
		return 'Files(filename={!r},challenge={!r})'.format(self.filename,self.challenge)

	def __str__(self):
		return self.__repr__()

	def to_dict(self):
		__challenge = self.challenge.to_dict()
		return {'id':self.id,'filname':self.filename,'challenge':self.challenge.name}

# Unbelievably unperformant way of using this but oh well.
# Better way may be to have multiple tables so that I can avoid full table scans as it is a many-to-many
# Relationship but I'll leave it be for now.
class HintsUnlocked(models.Model):
	user = models.ForeignKey('User',on_delete=models.CASCADE)
	hint = models.ForeignKey('Hints',on_delete=models.CASCADE)

	def __len__(self):
		return 1

	def __repr__(self):
		return "HintsUnlocked(user={!r},Hint={!r})".format(self.user,self.hint)

	def __str__(self):
		return self.__repr__()

	def to_dict(self):
		return {'id':self.id,'username':self.user.username,'user_id':self.user_id,'hint_id':self.hint_id}


class Hints(models.Model):
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='hints')
	description = models.TextField()
	level = models.IntegerField()
	#used = models.ManyToManyField(User)
	timestamp = models.DateTimeField(default=timezone.now)

	def __repr__(self):
		return 'Hints(challenge={!r},description={!r},level={!r},timestamp={!r}'.format(self.challenge,self.description,self.level,self.timestamp)

	def __str__(self):
		return self.__repr__()

	def __len__(self):
		return 1

	def to_dict(self):
		return {'id':self.id,'challenge_name':self.challenge.name,'description':self.description,'level':self.level}
