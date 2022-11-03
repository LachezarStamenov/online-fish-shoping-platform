from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('e_fish_shop_app.fish_shop.urls')),
    path('store/', include('e_fish_shop_app.store.urls')),
    path('cart/', include('e_fish_shop_app.cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
