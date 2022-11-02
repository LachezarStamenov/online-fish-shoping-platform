from django.urls import path

from e_fish_shop_app.store.views import store

urlpatterns = (
    path('', store, name='store'),
    path('<slug:category_slug>/', store, name='products by category'),
)