from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class SaveSlot(models.Model):
    slot_id = models.IntegerField(default=1)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    current_paragraph = models.IntegerField(default=1)
    character_state = models.JSONField(default=dict)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.player.username} | Slot id : {self.slot_id}'

@receiver(post_save, sender=User)
def gamestate_create(sender, instance=None, created=False, **kwargs):
    if created:
        SaveSlot.objects.create(player=instance, slot_id=1)
        SaveSlot.objects.create(player=instance, slot_id=2)
        SaveSlot.objects.create(player=instance, slot_id=3)