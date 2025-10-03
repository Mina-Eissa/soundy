from django.db import models 
import uuid
from ..validators import *
from ..models import Member,Track
def playlist_cover(instance, filename):
    ext = filename.split('.')[-1]
    return f"playlist_cover/{instance.owner.username}-{instance.name}.{ext}"

class Playlist(models.Model): 
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=100,validators=[validate_name])
    owner = models.OneToOneField(Member,on_delete=models.CASCADE)
    cover = models.ImageField(upload_to=playlist_cover,validators=[validate_image_mime],null=True,blank=True)
    tracks = models.ManyToManyField(Track,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name