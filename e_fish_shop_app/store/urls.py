from django.urls import path

from e_fish_shop_app.store.views import show_product_details, StoreView

urlpatterns = (
    path('', StoreView.as_view(), name='store'),
    path('<slug:category_slug>/', StoreView.as_view(), name='products by category'),
    path('<slug:category_slug>/<slug:product_slug>/', show_product_details, name='show product details'),

)