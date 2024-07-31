from django import forms

from .models import SteamAccount, ProSteamAccount


class SteamAccountForm(forms.ModelForm):
    class Meta:
        model = SteamAccount
        fields = '__all__'


class ProSteamAccountForm(forms.ModelForm):
    class Meta:
        model = ProSteamAccount
        fields = '__all__'
