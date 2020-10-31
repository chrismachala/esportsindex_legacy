from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from bootstrap_modal_forms.mixins import CreateUpdateAjaxMixin


class BuyForm(BSModalForm, CreateUpdateAjaxMixin):

   # def __init__(self, *args, **kwargs):
  #      super(BuyForm, self).__init__(*args, **kwargs)
   #     self.fields['volume'] = forms.IntegerField(max_value=)

    volume = forms.IntegerField(min_value=0)

