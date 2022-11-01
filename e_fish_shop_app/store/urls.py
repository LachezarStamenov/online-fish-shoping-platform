from django.urls import path

from e_fish_shop_app.store.views import StoreView

urlpatterns = (
    path('', StoreView.as_view(), name='store'),
)