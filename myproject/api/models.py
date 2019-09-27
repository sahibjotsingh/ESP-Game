from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
	locked_by = models.OneToOneField(User, related_name='locked_task', on_delete=models.CASCADE, blank=True, null=True, default=None)

	def __str__(self):
		return '%s' % self.id

class PrimaryImage(models.Model):
	image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
	task = models.ForeignKey(Task, related_name='primary_images', on_delete=models.SET_NULL, blank=True, null=True, default=None)
	num_of_answers = models.IntegerField(default=0)
	user = models.ManyToManyField(User, related_name='questions_answered', blank=True, null=True, default=None)

	def __str__(self):
		return '%s' % self.image.name

class SecondaryImage(models.Model):
	image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
	primary_image = models.ForeignKey(PrimaryImage, related_name='secondary_images', on_delete=models.CASCADE)
	is_a_match = models.BooleanField(default=False)

	def __str__(self):
		return '%s' % self.image.name

class UserResponse(models.Model):	
	is_a_match = models.BooleanField(default=None, null=True)
	image = models.ForeignKey(SecondaryImage, related_name='secondary_image_responses', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user_responses', on_delete=models.SET_NULL, blank=True, null=True, default=None)

	def __str__(self):
		return '%s' % self.image

class MyUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	points = models.IntegerField(default=0)
	non_matches = models.IntegerField(default=0)
	matches = models.IntegerField(default=0)

	def __str__(self):
		return '%s' % self.user		


	
	
