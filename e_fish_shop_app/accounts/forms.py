from django import forms

from e_fish_shop_app.accounts.models import Account


class RegistrationForm(forms.ModelForm):
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
