from django.contrib.auth.decorators import login_required
from django.urls import path

from e_fish_shop_app.accounts.views import login, LogoutView, activate, register, forgot_password, \
    reset_password, reset_password_validate, dashboard, my_orders

urlpatterns = (
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgotpassword/', forgot_password, name='forgot password'),
    path('resetpassword_validate/<uidb64>/<token>/', reset_password_validate, name='reset password validate'),
    path('resetpassword/', reset_password, name='reset password'),

    path('my_orders/', my_orders, name='may orders'),
)