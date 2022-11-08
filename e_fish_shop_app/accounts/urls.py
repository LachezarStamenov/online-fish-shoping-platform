from django.urls import path

from e_fish_shop_app.category.views import login, logout, RegistrationView

urlpatterns = (
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
)