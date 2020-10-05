from django.db import models


# Create your models here.
class Player(models.Model):
    player_id = models.IntegerField()
    ign = models.CharField("In Game Name", max_length=200)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    images = models.ForeignKey('Images', on_delete=models.CASCADE, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    stats = models.ForeignKey("Stats", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.ign


class SocialMedia(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)


class Images(models.Model):
    default = models.CharField(max_length=1000,
                               default="https://img.abiosgaming.com/other/New-Abios-Place-Holder.png")
    thumbnail = models.CharField(max_length=1000,
                                 default="https://img.abiosgaming.com/other/thumbnails/New-Abios-Place-Holder.png")


class Country(models.Model):
    country_id = models.IntegerField()
    name = models.CharField(max_length=60, blank=True)
    short_name = models.CharField(max_length=10)
    images = models.ForeignKey('Images', on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True)


class Region(models.Model):
    region_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    short_name = models.CharField(max_length=10, blank=True)


class Team(models.Model):
    team_id = models.IntegerField()
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=10, blank=True)
    images = models.ForeignKey('Images', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class PlayerTeam(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    def __str__(self):
        return self.player.ign + " plays for " + self.team.name


class Map(models.Model):
    map_id = models.IntegerField()
    name = models.CharField(max_length=150)
    images = models.ForeignKey('Images', on_delete=models.CASCADE)


class Stats(models.Model):
    kills = models.DecimalField(max_digits=16, decimal_places=13, blank=True, default=0)
    assists = models.DecimalField(max_digits=16, decimal_places=13, blank=True, default=0)
    flash_assists = models.DecimalField(max_digits=16, decimal_places=13, blank=True, default=0)
    death = models.DecimalField(max_digits=16, decimal_places=13, blank=True, default=0)
    dmg_give = models.DecimalField(max_digits=18, decimal_places=13, blank=True, default=0)
    dmg_taken = models.DecimalField(max_digits=18, decimal_places=13, blank=True, default=0)
    history = models.IntegerField(blank=True, default=0)
    accuracy = models.DecimalField(max_digits=14, decimal_places=13, blank=True, default=0)
    plant = models.DecimalField(max_digits=16, decimal_places=13, blank=True, default=0)
    defuse = models.DecimalField(max_digits=16, decimal_places=13, blank=True, default=0)


class Tournament(models.Model):
    tournament_id = models.IntegerField()
    title = models.CharField(max_length=200)
    tier = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    short_title = models.CharField(max_length=100, blank=True)


class Series(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    tier = models.IntegerField()
    best_of = models.IntegerField()
    tournament = models.ForeignKey('Tournament', on_delete=models.SET_NULL, null=True)
    postponed_from = models.DateTimeField(blank=True)
    scores = models.ForeignKey('Scores', on_delete=models.SET_NULL, null=True, related_name='scores')
    forfeit = models.ForeignKey('Scores', on_delete=models.SET_NULL, null=True, related_name='forfeit')
    teams = models.ForeignKey('Teams', on_delete=models.SET_NULL, null=True)


class Teams(models.Model):
    team1 = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, related_name='team1')
    team2 = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, related_name='team2')


class Scores(models.Model):
    team_1_score = models.IntegerField(null=True, blank=True)
    taam_2_score = models.IntegerField(null=True, blank=True)


class Match(models.Model):
    map = models.ForeignKey('Map', on_delete=models.SET_NULL, null=True)
    series = models.ForeignKey('Series', on_delete=models.SET_NULL, null=True)
    ct_stats = models.ForeignKey('Stats', on_delete=models.SET_NULL, null=True, related_name='ct_stats')
    t_stats = models.ForeignKey('Stats', on_delete=models.SET_NULL, null=True, related_name='t_stats')
    player = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True)