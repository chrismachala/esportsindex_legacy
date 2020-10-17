from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    credit = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def add_credit(self, value):
        self.credit += value
        self.save()

    def remove_credit(self, value):
        self.credit -= value
        self.save()


class Future(models.Model):
    asset = models.ForeignKey('esi_players.Player', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def is_empty(self):
        if self.quantity == 0:
            self.delete()
        else:
            return False


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()