from django.shortcuts import render

from e_fish_shop_app.accounts.forms import RegistrationForm


def register(request):

    form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return
