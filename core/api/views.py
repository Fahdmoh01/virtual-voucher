from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class OverviewAPI(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Welcome to the API!",
            "description": "This is a REST API for the eVoucher App.",
        })
