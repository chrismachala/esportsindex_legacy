from django.shortcuts import render, redirect
from .models import TransactionType, Transaction, Asset
from django.utils import timezone
from esi_players.models import Player
from esi_users.models import Future
from django.http import HttpResponseRedirect
from .forms import BuyForm


def get_transaction(request, ttype ,player_pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BuyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            volume = form.cleaned_data['volume']

            if ttype == 'Buy':

                buy_future(request, player_pk, volume)
            else:
                sell_future(request, player_pk, volume)

            return redirect('/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BuyForm()
        asset = Asset.objects.get(player_id=player_pk)

    return render(request, 'esi_pricingengine/transaction_form.html', {'form': form, 'asset': asset, 'ttype' : ttype})


def create_transaction(request, player_pk, volume):
    t = Transaction()
    t.asset = Asset.objects.get(player__id=player_pk)
    print("asset: {0}".format(t.asset.__str__()))
    t.user = request.user.profile
    # will need to get from POST
    t.volume = volume
    t.price_per_unit = t.asset.value
    # redundant below
    t.timestamp = timezone.now()
    return t


# Create your views here.
def buy_future(request, player_pk, volume):
    t = create_transaction(request, player_pk, volume)
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


def sell_future(request, player_pk, volume):
    t = create_transaction(request, player_pk, volume)
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
