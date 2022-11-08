from django.contrib.auth.decorators import login_required
from django.urls import path

from e_fish_shop_app.category.views import login, RegistrationView, LogoutView

urlpatterns = (
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
)