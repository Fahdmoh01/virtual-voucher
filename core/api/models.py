import uuid
import decimal
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.email if self.email else 'Anonymous'  # noqa

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'


class Event(models.Model):
    '''model For creating and storing Events'''

    def generate_event_id(self):
        '''generate a unique event id'''
        return f'EV{datetime.now().strftime("%Y%m%d%H%M%S%f")}'
    event_id = models.CharField(max_length=100, default=generate_event_id, unique=True)  # noqa
    name = models.CharField(max_length=200)
    date = models.DateField()
    participants = models.ManyToManyField(User, related_name="participants", blank=True)  # noqa
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_id + " - " + self.name


class Voucher(models.Model):
    '''model for creating and storing Vouchers'''

    def generate_voucher_id(self):
        '''generate a unique voucher id'''
        return f'VO{datetime.now().strftime("%Y%m%d%H%M%S%f")}'
    voucher_id = models.CharField(max_length=50, default=generate_voucher_id, unique=True)  # noqa
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # event_type = BASIC, PREMIUM, VIP
    event_type = models.CharField(max_length=50, default="BASIC")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.voucher_id


class EventVoucher(models.Model):
    '''model for creating and storing EventVoucher'''
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    redeemer = models.ForeignKey(User, on_delete=models.CASCADE)
    times_redeemed = models.IntegerField(default=0)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_redeemed(self) -> bool:
        '''For checking if a voucher has been redeemed already - returns True or False'''
        if self.voucher.event_type == "BASIC" and self.is_redeemed >= 1:
            return True
        elif self.voucher.event_type == "PREMIUM" and self.is_redeemed >= 2:
            return True
        elif self.voucher.event_type == "VIP" and self.is_redeemed >= 3:
            return True
        else:
            return False

    def redeem(self):
        '''Implements redeeming of voucher'''
        self.times_redeemed += 1
        self.save()

    def __str__(self):
        return self.voucher.voucher_id + " - " + self.redeemer.get_fullname()


class Wallet(models.Model):
    wallet_id = models.CharField(max_length=100, default=uuid.uuid4)
    main_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)  # noqa
    available_balance = models.DecimalField(decimal_places=2, max_digits=50, default=0.0)  # noqa
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def credit_wallet(self, amount):
        self.main_balance += decimal.Decimal(amount)
        self.available_balance += decimal.Decimal(amount)
        self.save()

    def debit_wallet(self, amount):
        self.main_balance -= decimal.Decimal(amount)
        self.available_balance -= decimal.Decimal(amount)
        self.save()

    def get_wallet_balance(self):
        return decimal.Decimal(self.main_balance)

    def __str__(self):
        return self.wallet_id
