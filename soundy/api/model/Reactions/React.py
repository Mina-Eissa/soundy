from django.db import models
import uuid
from api.model.Member import Member
from api.model.Track import Track

class React(models.Model):
    """
    React model that connects a Member with a Track
    and stores their reaction (like, love, etc.)
    """
    REACTION_CHOICES = [
        ("like", "👍 Like"),
        ("love", "❤️ Love"),
        ("fire", "🔥 Fire"),
        ("sad", "😢 Sad"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="reactions")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("member", "track")  # each member can react once per track

    def __str__(self):
        return f"{self.member.username} reacted {self.reaction} to {self.track.title}"