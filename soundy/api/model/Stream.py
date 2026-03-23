from django.db import models
from api.models import Member,Track
import uuid
class Stream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,verbose_name="Stream ID")
    member = models.ForeignKey('Member',on_delete=models.CASCADE,related_name='streams')
    track = models.ForeignKey('Track', on_delete=models.CASCADE,related_name='streams')
    started_at=models.DateTimeField(auto_now_add=True)
    last_position = models.IntegerField(default=0)
    is_counted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    class Meta:
        unique_together = ("member", "track")  # each member can react once per track
    def __str__(self):
        return f"Stream of {self.track.name} listen by {self.member.username}"