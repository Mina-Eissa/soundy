from django.db import models
from django.core.validators import FileExtensionValidator
import uuid
from ..models import Member
from ..validators import *
import os 
from mutagen import File
from datetime import timedelta
def track_audio(instance, filename):
    ext = filename.split('.')[-1]
    return f"tracks/{instance.name}.{ext}"
class Genre(models.TextChoices):
    POP = 'Pop', 'Pop'
    ROCK = 'Rock', 'Rock'
    JAZZ = 'Jazz', 'Jazz'
    CLASSICAL = 'Classical', 'Classical'
    HIPHOP = 'HipHop', 'HipHop'
    ELECTRONIC = 'Electronic', 'Electronic'
    COUNTRY = 'Country', 'Country'
    REGGAE = 'Reggae', 'Reggae'
    BLUES = 'Blues', 'Blues'
    METAL = 'Metal', 'Metal'
    FOLK = 'Folk', 'Folk'
    RNB = 'RnB', 'RnB'
    ARABIC = 'Arabic', 'Arabic'
    OTHER = 'Other', 'Other'   
    
class Track(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,verbose_name="Track ID")
    name = models.CharField(max_length=255, validators=[validate_name],verbose_name="Track Name")
    bio = models.TextField(validators=[validate_safe_text], blank=True, null=True,verbose_name="Track Bio")
    duration = models.DurationField(verbose_name="Track Duration")
    genre = models.CharField(max_length=50, choices=Genre.choices, default=Genre.OTHER,verbose_name="Track Genre")
    artist = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='tracks')
    cover = models.ImageField(upload_to='track_covers/',validators=[validate_image_mime],default='track_covers/audio_template.jpg')
    audio_file = models.FileField(upload_to=track_audio,validators=[FileExtensionValidator(allowed_extensions=['mp3','wav','flac','ogg','aac','m4a']),validate_audio_mime])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # auto-calc duration only if not set
        if self.audio_file:
            audio_path = self.audio_file.path
            if os.path.exists(audio_path):
                try:
                    audio_file = File(audio_path)
                    if audio_file.info.length :
                        seconds = int(audio_file.info.length)
                        self.duration = timedelta(seconds=seconds)
                    else:
                        self.duration = timedelta(0)
                except Exception as e:
                    print(f"Error extracting duration: {e}")
        super().save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        # Delete image file
        if self.cover and os.path.isfile(self.cover.path):
            os.remove(self.cover.path)

        # Delete audio file
        if self.audio_file and os.path.isfile(self.audio_file.path):
            os.remove(self.audio_file.path)

        # Delete instance
        super().delete(*args, **kwargs)