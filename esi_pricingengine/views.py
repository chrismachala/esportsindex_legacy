from django.contrib import messages
from django.shortcuts import render, redirect
from .models import TransactionType, Transaction, Asset
from django.utils import timezone
from esi_players.models import Player
from esi_users.models import Future
from django.http import HttpResponseRedirect
from .forms import BuyForm
from bootstrap_modal_forms.generic import BSModalFormView
from django.urls import reverse_lazy, reverse
from django import forms
from django.core.validators import MaxValueValidator

class TransactionView(BSModalFormView):
    template_name = 'esi_pricingengine/transaction_modal.html'
    form_class = BuyForm
    success_message = "Player purchased"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset = Asset.objects.get(player_id=self.kwargs['player_pk'])
        ttype = self.kwargs['ttype']
        context["asset"] = asset
        context["ttype"] = ttype
        return context
        # return None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initials = super(TransactionView, self).get_initial()
        initials['ttype'] = self.kwargs['ttype']
        initials['player_pk'] = self.kwargs['player_pk']

        return initials

    def form_valid(self, form):
        print(self.request.is_ajax())

        asset = Asset.objects.get(player__id=self.kwargs['player_pk'])


        print(asset.remaing_volume())
        print(asset.volume)
        print(form.fields['volume'].max_value)

        validator = MaxValueValidator(55)

        if form.is_valid():

            if self.request.is_ajax():

                volume = form.cleaned_data['volume']

                if self.kwargs['ttype'] == 'Buy':

                    t = buy_future(self.request, self.kwargs['player_pk'], volume)
                    #print(asset.proc_transaction(transaction=t))
                else:
                    t = sell_future(self.request, self.kwargs['player_pk'], volume)
                    #print(asset.proc_transaction(transaction=t))

            response = super().form_valid(form)
            print("Gettiing Response")

        return response

    def get_success_url(self):
        return reverse_lazy('home')


def get_transaction(request, ttype, player_pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BuyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            asset = Asset.objects.get(player_id=player_pk)
            volume = form.cleaned_data['volume']

            if ttype == 'Buy':

                t = buy_future(request, player_pk, volume)
                print(asset.proc_transaction(transaction=t))
            else:
                t = sell_future(request, player_pk, volume)
                print(asset.proc_transaction(transaction=t))

            return redirect('/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BuyForm()
        asset = Asset.objects.get(player_id=player_pk)

    return render(request, 'esi_pricingengine/transaction_form.html', {'form': form, 'asset': asset, 'ttype': ttype})


def create_transaction(request, player_pk, volume):
    print("Start Transaction")
    t = Transaction()
    t.asset = Asset.objects.get(player__id=player_pk)
    print("asset: {0}".format(t.asset.__str__()))
    t.user = request.user.profile
    # will need to get from POST
    t.volume = volume
    t.price_per_unit = t.asset.value
    # redundant below
    t.timestamp = timezone.now()
    print("Fin Transaction")
    return t


# Create your views here.
def buy_future(request, player_pk, volume):
    print("Start Buy")
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
    print("Fin Buy")
    return t


def sell_future(request, player_pk, volume):
    print("Start Sell")
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
    print("Fin Sell")
    return t
