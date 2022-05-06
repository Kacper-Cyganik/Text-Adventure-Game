from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class SaveSlot(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    current_paragraph = models.IntegerField(default=1)
    character_state = models.JSONField(default=dict)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.player.username} GameState'

@receiver(post_save, sender=User)
def gamestate_create(sender, instance=None, created=False, **kwargs):
    if created:
        SaveSlot.objects.create(player=instance,)