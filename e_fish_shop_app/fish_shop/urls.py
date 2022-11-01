from django.urls import path

from e_fish_shop_app.fish_shop.views import home

urlpatterns = (
    path('', home, name='home'),
)