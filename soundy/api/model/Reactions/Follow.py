from django.db import models
import uuid
from api.model.Member import Member

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="following"   # who this member is following
    )
    following = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="followers"   # who is following this member
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")  # prevent duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"