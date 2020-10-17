from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('player/<int:player_pk>', views.player, name='player')
]