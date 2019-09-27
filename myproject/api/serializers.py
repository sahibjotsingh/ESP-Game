from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username')

class SecondaryImageSerializer(serializers.HyperlinkedModelSerializer):
	image = serializers.ImageField(max_length = None, use_url=True)

	class Meta:
		model = SecondaryImage
		fields = ('id', 'image', 'is_a_match')

class SecondaryImageSerializer1(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = SecondaryImage
		fields = ('id', 'image', 'is_a_match')
		
		extra_kwargs = {
			'url': {'view_name': 'secondary_image_1-detail'}
		}


class PrimaryImageSerializer(serializers.HyperlinkedModelSerializer):
	image = serializers.ImageField(max_length = None, use_url=True)
	secondary_images = SecondaryImageSerializer1(many=True)

	class Meta:
		model = PrimaryImage
		fields = ('id', 'image', 'secondary_images', 'num_of_answers',)

# ->
class PrimaryImageSerializer2(serializers.HyperlinkedModelSerializer):
	image = serializers.ImageField(max_length = None, use_url=True)
	secondary_images = SecondaryImageSerializer1(many=True)
	user = UserSerializer(many=True)

	class Meta:
		model = PrimaryImage
		fields = ('id', 'image', 'secondary_images', 'num_of_answers', 'user')


class TaskSerializer(serializers.ModelSerializer):
	primary_images = PrimaryImageSerializer(many=True)

	class Meta:
		model = Task
		fields = ('id', 'primary_images', 'locked_by',)	


class TaskForUserSerializer(serializers.ModelSerializer):
	primary_images = PrimaryImageSerializer(many=True)

	class Meta:
		model = Task
		fields = ('id', 'primary_images',)	
		

class MyUserSerializer(serializers.ModelSerializer):

	class Meta:
		model = MyUser
		fields = ('user', 'points', 'non_matches', 'matches')


"""
class UserSerializer(serializers.ModelSerializer):
	questions_answered = TaskSerializer()

	class Meta:
		model = User
		fields = ('username', 'questions_answered')
"""