from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('adminsecured/', admin.site.urls),
    path('', include('e_fish_shop_app.fish_shop.urls')),
    path('store/', include('e_fish_shop_app.store.urls')),
    path('cart/', include('e_fish_shop_app.cart.urls')),
    path('accounts/', include('e_fish_shop_app.accounts.urls')),
    path('orders/', include('e_fish_shop_app.orders.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
