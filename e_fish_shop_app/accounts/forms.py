from django import forms

from e_fish_shop_app.accounts.helpers import BootstrapFormMixin
from e_fish_shop_app.accounts.models import Account


class RegistrationForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password'
            }
        ))

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat Password'
            }
        ))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']


