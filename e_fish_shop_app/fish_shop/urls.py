from django.urls import path

from e_fish_shop_app.fish_shop.views import HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
)
