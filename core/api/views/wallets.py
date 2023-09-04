from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Event, User
from api.serializers import EventsSerializer
from django.utils.decorators import method_decorator
from core.utils.decorators import OrganizerOnly,AppUserOnly

class FundWalletAPI(APIView):
	'''Used to simulate user's topup of wallet'''
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request, *args, **kwargs):
		user = request.user
		amount = request.data.get('amount')
		try:
			user.fund_wallet(amount)
		except Exception as er:
			print(er)
			return Response({
				"message": str(er),
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			return Response({
				"message":"Wallet Funded Successfully"
			}, status=status.HTTP_200_OK)
		

class WithdrawFromWalletAPI(APIView):
	'''Used to simulate user's withdrawal of funds wallet'''
	permission_classes = (permissions.IsAuthenticated,)
	
	def post(self, request, *args, **kwargs):
		user = request.user
		amount = request.data.get('amount')
		try: 
			user.withdraq_wallet(amount)
		except Exception as er:
			print(er)
			return Response({
				"message":str(er),
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			return Response({
				"message": "Funds Withdrawn Successfully"
			}, status=status.HTTP_200_OK)