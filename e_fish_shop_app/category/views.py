from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from e_fish_shop_app.accounts.forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from e_fish_shop_app.accounts.models import Account

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


class RegistrationView(views.CreateView):
    model = Account
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        # Email Activation Setup
        current_site = get_current_site(self.request)
        subject = 'Please activate your account.'
        message = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        user.email_user(subject=subject, message=message)

        # Success registration message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Check Your Email For Account Activation Link'
        )

        return super().form_valid(form)





class LogoutView(SuccessMessageMixin, auth_views.LogoutView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        messages.add_message(self.request, messages.INFO, 'You are logged out.')



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    return render(request, 'accounts/login.html')


def activate(request):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
