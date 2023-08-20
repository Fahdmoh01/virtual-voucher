from django.contrib.auth import login
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Event, EventVoucher, User, Voucher
from django.utils.decorators import method_decorator
from core.utils.decorators import OrganizerOnly, RestaurantOnly



class SystemStatsAPI(APIView):
	'''For getting statis on vouchers'''
	permission_classes = (permissions.IsAuthenticated,)
	
	# still thinking about this
	def get(self, request, *args, **kwargs):
		'''Uses get request to relevant statistics on vouchers'''
		user = request.user
		
		#get total vouchers broadcasted participants
		event_vouchers = EventVoucher.objects.filter(created_by=user)
		silver_broadcast = event_vouchers.filter(voucher__voucher_type="SILVER") # noqa
		gold_broadcast = event_vouchers.filter(voucher__voucher_type="GOLD") # noqa 
		diamond_broadcast = event_vouchers.filter(voucher__voucher_type="DIAMOND") # noqa

		# count total broadcasted vouchers by type
		all_broadcast_count = event_vouchers.count()
		silver_broadcast_count = silver_broadcast.count()
		gold_broadcast_count = gold_broadcast.count()
		diamond_broadcast_count = diamond_broadcast.count()

		# get counts of redeemed vouchers by type
		all_redeemed_count = len([v for v in  event_vouchers if v.is_redeemed()]) # noqa 
		silver_redeemed = len ([v for v in silver_broadcast if v.is_redeemed()]) # noqa
		gold_redeemed = len([v for v in gold_broadcast if v.is_redeemed()]) # noqa
		diamond_redeemed = len([v for v in diamond_broadcast if v.is_redeemed()]) # noqa

		# get the total types of vouchers created by users
		silver_vouchers = Voucher.objects.filter(created_by=user, voucher_type="SILVER")# noqa 
		gold_vouchers = Voucher.objects.filter(created_by=user, voucher_type="GOLD")# noqa
		diamond_vouchers = Voucher.objects.filter(created_by=user, voucher_type="DIAMOND")# noqa

		# count the total vouchers created by user by types
		silver_count = silver_vouchers.count()
		gold_count = gold_vouchers.count()
		diamond_count = diamond_vouchers.count()

		# all vouchers ever created by user. All types included
		vouchers_created = Voucher.objects.filter(created_by=user).count()

		res ={
			"created":{
				"all": vouchers_created,
				"silver": silver_count,
				"gold": gold_count,
				"diamond": diamond_count,
			},
			"broadcasted":{
				"all": all_broadcast_count,
				"silver": silver_broadcast_count,
				"gold": gold_broadcast_count,
				"diamond": diamond_broadcast_count,
			},
			"redeemed":{
				"all": all_redeemed_count,
				"silver": silver_redeemed,
				"gold": gold_redeemed,
				"diamond": diamond_redeemed,
			}
		}

		return Response({
			"stats":res
		},status=status.HTTP_200_OK)


class BroadcastVoucherAPI(APIView):
	'''Broadcast voucher to event participants'''

	permission_classes = [permissions.IsAuthenticated]

	@method_decorator(OrganizerOnly)
	def post(self, request, *args, **kwargs):
		'''Uses post request to broadcast voucher to event participants'''

		user = request.user
		voucher_id = request.data.get("voucher_id")
		event_id = request.data.get("event_id")

		voucher = Voucher.objects.filter(voucher_id=voucher_id) # noqa
		event = Event.objects.filter(created_by=user, id=event_id) # noqa

		if(voucher is None) or (event is None):
			return Response({
				"message": "Voucher or Event is Invalid"
			}, status=status.HTTP_404_NOT_FOUND)
		else:
			event_vouchers = []
			participants = event.participants.all()
			for participant in participants:
				ev = EventVoucher(voucher=voucher, redeemer=participant, created_by=user) # noqa
				event_vouchers.append(ev)
			EventVoucher.objects.bulk_create(event_vouchers)
			return Response({
				"message":"Vouchers Broadcasted Successfully"
			},status=status.HTTP_200_OK)


class RedeemVoucherApI(APIView):
	'''Redeem voucher for event participant by restaurant'''

	permission_classes = (permissions.IsAuthenticated,)

	@method_decorator(RestaurantOnly)
	def post(self, request, *args, **kwargs):
		'''Uses post request to redeem voucher for event participant by restaurant''' # noqa
		user = request.user 
		voucher_id = request.data.get("voucher_id")
		voucher = Voucher.objects.filter(id=voucher_id).first()

		redeemer_email = request.data.get("redeemer_email")
		redeemer = User.objects.filter(email= redeemer_email)

		event_voucher = EventVoucher.objects.filter(voucher=voucher, redeemer=redeemer).first() # noqa
		if event_voucher.is_redeemed():
			return Response({
				"message": "Voucher Already Redeemed"
			}, status= status.HTTP_400_BAD_REQUEST)
		else:
			event_voucher.redeem(user)
			return Response({
				"message": "Voucher Redeemed Successfully"
			}, status=status.HTTP_200_OK)
		


class RevokeRedeemersVoucherAPI(APIView):
	'''Revoke voucher from event participants'''

	permission_classes = (permissions.IsAuthenticated,)

	@method_decorator(OrganizerOnly)
	def delete(self, request, *args, **kwargs):
		'''Uses delete requeste to revoke participants voucher'''
		user = request.user
		voucher_id = request.data.get("voucher_id")
		voucher = Voucher.objects.filter(id=voucher_id, created_by=user).first()

		redeemer_email = request.data.get("redeemer_email")
		redeemer = User.objects.filter(email=redeemer_email).first()

		event_voucher = EventVoucher.objects.filter(redeemer=redeemer, voucher=voucher).first()
		if event_voucher is not None:
			event_voucher.delete()
			return Response({
				"message": "Voucher Revoked Successfully"
			}, status=status.HTTP_200_OK)
		else:
			return Response({
				"message":"Voucher Not Found"
			}, status=status.HTTP_404_NOT_FOUND)