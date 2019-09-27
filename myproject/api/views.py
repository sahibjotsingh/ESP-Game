from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .serializers import *
from .models import *
from rest_framework_extensions import mixins
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import F

class PrimaryImageViewSet(mixins.NestedViewSetMixin, viewsets.ModelViewSet):
	queryset = PrimaryImage.objects.all()
	permission_classes = (IsAdminUser,)
	serializer_class = PrimaryImageSerializer2

class SecondaryImageViewSet(mixins.NestedViewSetMixin, viewsets.ModelViewSet):
	queryset = SecondaryImage.objects.all()
	permission_classes = (IsAdminUser,)
	serializer_class = SecondaryImageSerializer

class TaskViewSet(viewsets.ModelViewSet):
	queryset = Task.objects.all()
	permission_classes = (IsAdminUser,)
	serializer_class = TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()	
	permission_classes = (IsAuthenticated,)
	serializer_class = UserSerializer

class MyUserViewSet(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = MyUser.objects.all()
	serializer_class = MyUserSerializer 

	# returns a new-task.
	# 1. make a task with questions(primary images) which have the following conditions
	#		a. no question is already answered by current authenticated user
	#		b. no question is already used in some other Task
	# 		c. no. of answers for that question < 2
	# 2. if task has atleast n questions then it can be solved otherwise discard it
	# 3. lock the task 
	@action(detail=True, methods=['get'], url_path='get-task')
	def get_task(self, request, pk=None):
		user = self.request.user
		questions_answered = user.questions_answered.all()
		
		task = Task.objects.create()
		n = 2 # change this to make a task of 5 questions 
		for i in range(n):

			if PrimaryImage.objects.filter(num_of_answers=1, task=None).exclude(id__in=questions_answered).count() > 0:
			
				primary_image = PrimaryImage.objects.filter(num_of_answers=1, task=None).exclude(id__in=questions_answered).order_by('?').first()

				primary_image.task = task
			
				primary_image.save()
			
			elif PrimaryImage.objects.filter(num_of_answers=0, task=None).exclude(id__in=
				questions_answered).count() > 0:
				
				primary_image = PrimaryImage.objects.filter(num_of_answers=0, task=None).exclude(id__in=questions_answered).order_by('?').first()
				
				primary_image.task = task
				
				primary_image.save()

		if task.primary_images.count() >= n:
			task.locked_by = self.request.user
			task.save()
			primary_images = PrimaryImage.objects.filter(task=task)
			for primary_image in primary_images.iterator():
				secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
				for secondary_image in secondary_images.iterator():
					user_response = UserResponse.objects.create(image=secondary_image, user=self.request.user, is_a_match=None)

			serializer = TaskSerializer(task)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			task.delete()
			return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

	# Keep track of answers marked by authenticated user
	@action(detail=True, methods=['get'], url_path='track-game/match/(?P<si_pk>\d+)')
	def track_game_match(self, request, pk=None, si_pk=None):
		try:	
			secondary_image = SecondaryImage.objects.get(pk=si_pk)
			user_response = UserResponse.objects.filter(image=secondary_image, user=self.request.user).update(is_a_match=True)
			return Response({"status": "ok"}, status=status.HTTP_200_OK)
		except:
			return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

	# Keep track of answers un-marked by authenticated user
	@action(detail=True, methods=['get'], url_path='track-game/unmatch/(?P<si_pk>\d+)')
	def track_game_unmatch(self, request, pk=None, si_pk=None):
		try:	
			secondary_image = SecondaryImage.objects.get(pk=si_pk)
			user_response = UserResponse.objects.filter(image=secondary_image, user=self.request.user).update(is_a_match=False)
			return Response({"status": "ok"}, status=status.HTTP_200_OK)
		except:
			return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

	# End a task.
	# 1. if all questions were answered for a task then continue otherwise discard user responses
	# 2. for each question of this task
	# 		2.1. if question was not answered before then make users answers as final
	#		2.2. if question was answered before then 
	#				2.2.1. if answers given by both users (previous and current) match then give a point to both users and do not delete their answers
	#				2.2.2. if answers given by both users (previous and current) do match then delete their answers	and also mark final answer as false
	@action(detail=True, methods=['get'], url_path='end-task')
	def end_task(self, request, pk=None):
		task = Task.objects.get(locked_by=self.request.user)
		primary_images = PrimaryImage.objects.filter(task=task)

		all_answered = True
		for primary_image in primary_images:
			secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
			for secondary_image in secondary_images:
				user_response = UserResponse.objects.get(image=secondary_image, user=self.request.user)
				if user_response.is_a_match is None:
					all_answered = False
					break

		if all_answered is False:
			for primary_image in primary_images:
				secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
				for secondary_image in secondary_images:
					UserResponse.objects.get(image=secondary_image, user=self.request.user).delete()

		else:
			for primary_image in primary_images:
				primary_image.user.add(self.request.user)
				if primary_image.num_of_answers == 0:
					primary_image.num_of_answers=primary_image.num_of_answers+1
					primary_image.save()
					secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
					for secondary_image in secondary_images:
						secondary_image.is_a_match = UserResponse.objects.get(image=secondary_image, user=self.request.user).is_a_match
						secondary_image.save()

				elif primary_image.num_of_answers == 1:
					user1=None
					user2=None
					secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
					answers_match = True
					for secondary_image in secondary_images:
						user_responses = UserResponse.objects.filter(image=secondary_image).order_by('-id')[:2]
						user1 = user_responses[0].user
						user2 = user_responses[1].user
						if secondary_image.is_a_match != UserResponse.objects.get(image=secondary_image, user=self.request.user).is_a_match:
							secondary_image.is_a_match = False
							answers_match = False

					myuser1 = MyUser.objects.get(user=user1)
					myuser2 = MyUser.objects.get(user=user2)
					if answers_match == True:
						myuser1.points=myuser1.points+1	
						myuser1.matches=myuser1.matches+1	
						myuser1.save()			
						myuser2.points=myuser2.points+1				
						myuser2.matches=myuser2.matches+1	
						myuser2.save()	
						primary_image.num_of_answers=primary_image.num_of_answers+1
						primary_image.save()
					else:
						myuser1.non_matches=myuser1.non_matches+1	
						myuser1.save()			
						myuser2.non_matches=myuser2.non_matches+1	
						myuser2.save()			

						secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
						for secondary_image in secondary_images.iterator():
							UserResponse.objects.filter(image=secondary_image, user=user1).delete()
							UserResponse.objects.filter(image=secondary_image, user=user2).delete()

						primary_image.num_of_answers=0
						primary_image.save()

		task.delete()
		if all_answered is True:
			return Response({"message": "ok"}, status=status.HTTP_200_OK)
		else:
			return Response({"message": "discarded"}, status=status.HTTP_200_OK)

	# End the game
	@action(detail=True, methods=['get'], url_path='end-game')
	def end_game(self, request, pk=None):
		try:
			task = Task.objects.get(locked_by=self.request.user)	

			if task is not None:
				primary_images = PrimaryImage.objects.filter(task=task)
				for primary_image in primary_images:
					secondary_images = SecondaryImage.objects.filter(primary_image=primary_image)
					for secondary_image in secondary_images:
						UserResponse.objects.get(image=secondary_image, user=self.request.user).delete()
				task.delete()
		finally:
			return Response({"status": "ok"}, status=status.HTTP_200_OK)