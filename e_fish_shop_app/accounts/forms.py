from django import forms

from e_fish_shop_app.accounts.helpers import BootstrapFormMixin
from e_fish_shop_app.accounts.models import Account


class RegistrationForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def clean(self):
        clean_data = super(RegistrationForm, self).clean()
        password = clean_data.get('password')
        repeat_password = clean_data.get('repeat_password')

        if not password == repeat_password:
            raise forms.ValidationError(
                "Password does not match! Please try again!"
            )

    def save(self, commit=True):
        username = self.cleaned_data['email'].split("@")[0]
        profile = Account(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            username=username,
        )
        profile.phone_number = self.cleaned_data['phone_number']

        if commit:
            profile.save()
        return profile


