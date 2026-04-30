from django.db import models
from api.models import Track,Member



class Play(models.Model):
    track = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='plays')
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='plays')
    timestamp = models.DateTimeField(auto_now_add=True,db_index=True)

    def __str__(self):
        return f"{self.member.username} played {self.track.name} at {self.timestamp}"