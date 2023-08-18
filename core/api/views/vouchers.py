from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Voucher
from api.serializers import VoucherSerializer

class VoucherListAPI(APIView):
	'''For getting all vouchers created by the user'''
	permission_classes = (permissions.IsAuthenticated,)
	
	def get(self, request, *args, **kwargs):
		'''Uses get request to fetch all vouchers created by the user'''
		user = request.user
		voucher = Voucher.objects.filter(created_by=user).order_by("-id")
		serializer = VoucherSerializer(voucher, many=True)
		return Response({
			"vouchers": serializer.data,
		}, status=status.HTTP_200_OK)
	

class CUDVoucherAPI(APIView):
	'''For Create, Update, Delete of vouchers'''
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		'''Uses the post request to create a new voucher'''
		user = request.user
		amount = request.data.get("amount")
		voucher_type = request.data.get("voucher_type")

		voucher = Voucher.objects.create(
			amount=amount,
			voucher_type=voucher_type,
			created_by = user,
		)
		serializer = VoucherSerializer(voucher, many = False)
		return Response({
			"voucher":serializer.data,
		},status=status.HTTP_201_CREATED)
	

	def put(self, request, *args, **kwargs):
		'''Uses the put request to update the voucher'''
		user = request.user
		voucher_id = request.data.get("voucher_id")
		voucher = Voucher.objects.filter(id = voucher_id, created_by=user).first() #noqa
		amount = request.data.get("amount")
		voucher_type = request.data.get("voucher_type")

		if voucher is not None:
			voucher.amount = amount
			voucher.voucher_type = voucher_type

			voucher.save()
			serializer = VoucherSerializer(voucher, many=False)
			return Response({
				"voucher":serializer.data,
			},status = status.HTTP_200_OK)
		else:
			return Response({
				"message": "Voucher Not Found",
			},status=status.HTTP_404_NOT_FOUND)
		

	
	def delete(self, request, *args, **kwargs):
		'''Uses the delete request to delete an event'''
		user = request.user
		voucher_id = request.data.get("voucher_id")
		voucher = Voucher.objects.filter(id=voucher_id, created_by=user).first()
		if voucher is not None:
			voucher.delete()
			return Response({
				"message": "Voucher Deleted Successfully",
			}, status=status.HTTP_200_OK)
		else:
			return Response({
				"message":"Voucher Not Found"
			}, status=status.HTTP_404_NOT_FOUND)
		



