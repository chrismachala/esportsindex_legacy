from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=150, required=True, help_text="Email")
    first_name = forms.CharField(max_length=100, required=True, help_text="First Name")
    last_name = forms.CharField(max_length=100, required=True, help_text="Last Name")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user