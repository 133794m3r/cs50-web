from django.db import models
from django.contrib.auth.models import AbstractUser



# User model is just here so I can reference it, I use the default model.
class User(AbstractUser):
	pass


class Categories(models.Model):
	name = models.CharField(max_length=50)
	# def __dict__(self):
	# 	return {'id':self.id,'name':self.name}
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

	# def __dict__(self):
	# 	return {'id':self.id,'category':self.category,'points':self.points,'description':self.description,'flag':self.flag}

	def __repr__(self):
		return 'Challenges(id={!r},category={!r},points={!r},name={!r},description={!r},flag={!r}'.format(self.id,self.category,self.points,self.name,self.description,self.flag)

	def __str__(self):
		return self.__repr__()

	def to_dict(self):
		return {'id':self.id,'category':self.category.name,'name':self.name,'points':self.points,'description':self.description,'flag':self.flag}

	def __len__(self):
		return 1

class Solves(models.Model):
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='solves')
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='solves')

	def to_dict(self):
		__chal = self.challenge.to_dict()
		__user == self.user.to_dict()
		return {'challenge':{'id':__chal.id,'name':__chal.name},'user':__user.name}


	def __repr__(self):
		return 'Solves(challenge={!r},user={!r})'.format(self.challenge,self.user)


	def __str__(self):
		return self.__repr__()


	def __len__(self):
		return 1


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

class Hints(models.Model):
	challenge = models.ForeignKey('Challenges',on_delete=models.CASCADE,related_name='hints')
	description = models.TextField()
	hidden = models.BooleanField(default=True)
	level = models.IntegerField()
	used = models.ManyToManyField(User)

	def __repr__(self):
		return 'Hints(challenge={!r},description={!r},hidden={!r},level={!r},used={!r}'.format(self.challenge,self.description,self.hidden,self.self.level,self.used)

	def __str__(self):
		return self.__repr__()

	def __len__(self):
		return 1

	# def to_dict(self):
	# 	__challenge_name = self.challenge.to_dict()['name']
	# 	__used = self.used.to_dict()
	# 	return {'id':self.id}