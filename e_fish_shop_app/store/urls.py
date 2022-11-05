from django.urls import path

from e_fish_shop_app.store.views import show_product_details, store, SearchView

urlpatterns = (
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='products by category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', show_product_details, name='show product details'),
    path('search/', SearchView.as_view(), name='search')

)