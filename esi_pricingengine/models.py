from django.db import models
from django.utils import timezone
from enum import Enum
from esi_users.models import Future, Profile
# Create your models here.


class Asset(models.Model):
    """ A future/asset : holds the asset link ( player ) and how many futures are in circulation (volume) """
    player = models.ForeignKey('esi_players.Player', on_delete=models.CASCADE)
    volume = models.IntegerField(default=100, null=False)
    value = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    def __str__(self):
        return self.player.__str__()

    def generate_price(self):
        self.value = 1.00

    def proc_transaction(self, transaction):
        self.volume = (self.volume + transaction.volume) if transaction.type == TransactionType.B\
            else (self.volume - transaction.volume)

        self.generate_price()


class TransactionType(Enum):
    B = "Buy"
    S = "Sell"


class Transaction(models.Model):
    """ Whenever a user purchases a future a transaction is created """
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    user = models.ForeignKey('esi_users.Profile', on_delete=models.CASCADE)
    volume = models.IntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    timestamp = models.DateTimeField(null=False, default=timezone.now)
    type = models.CharField(max_length=255, choices=[(t_type, t_type.value) for t_type in TransactionType], null=True)
    valid = models.BooleanField(default=False)

    def is_valid(self):
        if self.type == TransactionType.B:
            return self.price_per_unit*self.volume <= self.user.credit
        else:
            if self.future_exist():
                return self.volume <= Future.objects.get(asset=self.asset, user=self.user).quantity
            else:
                return False

    def create_future(self):
        f = Future()
        f.user = self.user
        f.asset = self.asset
        f.quantity = self.volume
        f.save()

    def update_future(self):
        f = Future.objects.get(asset=self.asset, user=self.user)
        f.quantity = f.quantity + self.volume if self.type == TransactionType.B else f.quantity - self.volume
        f.save()

    def future_exist(self):
        f_count = Future.objects.filter(asset=self.asset, user=self.user).count()

        if f_count == 0:
            return False
        else:
            return True

# class AssetHistory(models.Model):
#     """ AssetHistory contains the average value of an asset on any given day """
#     asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
#     volume = models.IntegerField(default=100, null=False)
#     timestamp = models.DateTimeField(null=False, default=timezone.now)
#
#     def return_asset_transaction_list(self):
#         asset_transaction_list = AssetTransaction.objects.filter(asset=self.asset, timestamp=timezone.now())
#         return asset_transaction_list()
#
#     def calculate_volume(self):
#         """ The volume in an asset history is the average volumes of all transactions within the day """
#         temp = 0
#         asset_transaction_list = self.return_asset_transaction_list()
#         for asset_transaction in asset_transaction_list:
#             temp += asset_transaction.new_volume
#
#         self.volume = temp / len(asset_transaction_list)
#
#
# class AssetTransaction(models.Model):
#     """ Whenever a future is purchased an AssetTransaction is created to record daily averages """
#     transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
#     asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
#     new_volume = models.IntegerField()
#     timestamp = models.DateTimeField(null=False, default=timezone.now)
#






