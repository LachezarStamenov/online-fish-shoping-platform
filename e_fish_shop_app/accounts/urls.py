from django.urls import path

from e_fish_shop_app.category.views import login, register, logout

urlpatterns = (
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
)