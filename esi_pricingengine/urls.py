from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:player_pk>', views.buy_future, name='buy'),
    path('sell/<int:player_pk>', views.sell_future, name='sell')
]