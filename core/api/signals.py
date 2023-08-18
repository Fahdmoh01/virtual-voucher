from api.models import User,Wallet

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
	if created:
		#only create wallets for new restaurants and organizers
		if instance.is_restaurant() or instance.is_organizer():
			Wallet.objects.create(owner=instance)
	else:
		#create wallet for old restaurants/organizes who don't have wallets
		current_wallet = Wallet.objects.filter(owner=instance).first()
		if current_wallet is None:
			Wallet.objects.create(owner=instance)
			


