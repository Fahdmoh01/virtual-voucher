from typing import Any
from rest_framework import status
from rest_framework.response import Response

class OrganizerOnly(object):
	'''Decorator to check if user is an event organizer'''
	
	def __init__(self, original_method):
		self.original_method = original_method
		
	def __call__(self, request, *args, **kwargs):
		if (request.user.is_authenticated) and (request.user.role == "ORGANIZER"):
			return self.original_method(request, *args, **kwargs)
		else:
			return Response({
				"message": "Access Denied!"
			}, status=status.HTTP_403_FORBIDDEN)
		

class RestaurantOnly(object):
	'''Decorator to check if user is a restaurant'''

	def __init__(self, original_method):
		self.original_method = original_method

	def __call__(self, request, *args, **kwargs):
		if(request.user.is_authenticated) and (request.user.role == "RESTAURANT"):
			return self.original_method(request, *args, **kwargs)
		else:
			return Response({
				"message": "Access Denied!"
			}, status=status.HTTP_403_FORBIDDEN)


class AppUserOnly(object):
	'''Decorator to check if user is an app user'''

	def __init__(self, original_method):
		self.original_method = original_method


	def __call__(self, request, *args, **kwargs):
		if (request.user.is_authenticated) and (request.user.role == "APP_USER"):
			return self.original_method(request, *args, **kwargs)
		else:
			return Response({
				"message": "Access Denied!"
			}, status=status.HTTP_403_FORBIDDEN)
	

class AdminOnly(object):
	'''Decorator to check if logged-in user is an admin'''

	def __init__(self, original_method):
		self.original_method = original_method

	def __call__(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_staff: #noqa
				return self.original_method(request, *args, **kwargs)
			else:
				return Response({
					"message": "Access Denied!"
				}, status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({
				"message": "Access Denied!"
			}, status= status.HTTP_403_FORBIDDEN)
