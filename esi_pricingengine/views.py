from django.shortcuts import render, redirect
from .models import TransactionType, Transaction, Asset
from django.utils import timezone
from esi_players.models import Player
from esi_users.models import Future
from django.http import HttpResponseRedirect


def create_transaction(request, player_pk):
    t = Transaction()
    t.asset = Asset.objects.get(player__id=player_pk)
    print("asset: {0}".format(t.asset.__str__()))
    t.user = request.user.profile
    # will need to get from POST
    t.volume = 1
    t.price_per_unit = t.asset.value
    # redundant below
    t.timestamp = timezone.now()
    return t


# Create your views here.
def buy_future(request, player_pk):
    t = create_transaction(request, player_pk)
    t.type = TransactionType.B
    t.save()
    t.valid = t.is_valid()
    t.save()

    if t.valid:
        if t.future_exist():
            t.update_future()
            t.user.credit = t.user.remove_credit(t.volume * t.price_per_unit)
        else:
            t.create_future()
            t.user.credit = t.user.remove_credit(t.volume * t.price_per_unit)
    else:
        print("Not Enough credit")
    t.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def sell_future(request, player_pk):
    t = create_transaction(request, player_pk)
    t.type = TransactionType.S
    t.save()
    t.valid = t.is_valid()
    t.save()

    if t.valid:
        t.update_future()
        t.user.credit = t.user.add_credit(t.volume * t.price_per_unit)
        Future.objects.get(asset=t.asset, user=t.user).is_empty()
    else:
        print("Not Enough Futures")
    t.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
