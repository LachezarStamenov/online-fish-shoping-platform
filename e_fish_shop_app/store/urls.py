from django.urls import path

from e_fish_shop_app.store.views import store, SearchView, ProductDetailsView

urlpatterns = (
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='products by category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', ProductDetailsView.as_view(), name='show product details'),
    path('search/', SearchView.as_view(), name='search')

)