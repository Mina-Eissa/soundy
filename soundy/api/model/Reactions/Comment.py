from django.db import models
import uuid
from api.validators import validate_safe_text
from api.model.Track import Track
from api.model.Member import Member
class Comment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,verbose_name="Comment ID")
    content = models.TextField(validators=[validate_safe_text],verbose_name="Comment Content")
    track = models.ForeignKey(Track,on_delete=models.CASCADE,related_name="comments")
    member = models.ForeignKey(Member,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated At")
    
    def __str__(self):
        return f"Comment from {self.member.username} on track {self.track.name} \"{self.content}\""