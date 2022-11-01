from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from e_fish_shop_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('e_fish_shop_app.fish_shop.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
