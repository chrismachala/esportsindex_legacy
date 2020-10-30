from django import forms


class BuyForm(forms.Form):
    volume = forms.IntegerField(min_value=0, max_value=150)

