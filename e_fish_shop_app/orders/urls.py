from django.urls import path

from e_fish_shop_app.orders.views import place_order

urlpatterns = (
    path('place_order/', place_order, name='place order'),
)
