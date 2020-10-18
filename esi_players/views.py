from django.shortcuts import render, get_object_or_404
from django.views import generic
from esi_players.models import Player, Team, PlayerTeam
from django.http import HttpResponse
from esi_pricingengine.models import Asset

# Create your views here.


def index(request):
    return render(request, 'esi_players/index.html')


def players(request):
    template_name = 'esi_players/players.html'
    asset_list = Asset.objects.all()

    return render(request, template_name,
                  {'assets': asset_list})


def player(request, player_pk):
    asset = Asset.objects.get(player_id=player_pk)
    player_ins = Player.objects.filter(id=player_pk).first()
    team = PlayerTeam.objects.filter(player__player_id=player_ins.player_id).first().team
    template_name = 'esi_players/player.html'

    team_list = []
    for pt in PlayerTeam.objects.filter(team=team):
        if pt.player.player_id != player_ins.player_id:
            team_list.append(pt.player)

    return render(request, template_name, {'player': player_ins,'asset':asset, 'team': team, 'team_list':team_list})

