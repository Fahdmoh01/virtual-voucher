from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import RegisterSerializer, UserSerializer


class LoginAPI(KnoxLoginView):
	'''For handling user logins'''
	permission_classes = [permissions.AllowAny]

	def post(self, request, format=None):
		'''Uses the post method to login the user'''
		serializer = AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		login(request, user)
		# Delete token - this will logout any other users using this account
		AuthToken.objects.filter(user=user).delete()
		return Response({
			"user": UserSerializer(user).data,
			"token": AuthToken.objects.create(user)[1],
		}, status=status.HTTP_200_OK)


class SignUpAPI(generics.GenericAPIView):
	'''This CBV is used to register a new user'''
	permission_classes = [permissions.AllowAny]
	serializer_class = RegisterSerializer

	def post(self, request, *args, **kwargs):
		serializer = RegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response({
			"user": UserSerializer(user).data,
			"token": AuthToken.objects.create(user)[1],
		}, status=status.HTTP_201_CREATED)

