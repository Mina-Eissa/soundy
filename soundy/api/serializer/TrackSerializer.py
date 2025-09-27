from rest_framework import serializers
from ..models import Track,Member
from ..serializers import MemberSerializer

from mutagen import File as MutagenFile
from datetime import timedelta
import os

class TrackSerializer(serializers.ModelSerializer):
    # Show nested artist details (read-only)
    artist = MemberSerializer(read_only=True)

    # Accept artist by id when writing
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        source="artist",
        write_only=True
    )
    duration = serializers.DurationField(required=False)
    class Meta:
        model = Track
        fields = '__all__'
    
    def create(self, validated_data):
        audio_file = validated_data.get("audio_file")

        # Save the track first (so file exists on disk)
        track = super().create(validated_data)

        # Calculate duration if audio file is provided
        if audio_file and os.path.exists(track.audio_file.path):
            try:
                audio = MutagenFile(track.audio_file.path)
                if audio.info.length:
                    seconds = int(audio.info.length)
                    track.duration = timedelta(seconds=seconds)
                    track.save(update_fields=["duration"])
            except Exception as e:
                print(f"Error extracting duration: {e}")

        return track

    def update(self, instance, validated_data):
        # Same logic for updates
        audio_file = validated_data.get("audio_file", None)

        track = super().update(instance, validated_data)

        if audio_file and os.path.exists(track.audio_file.path):
            try:
                audio = MutagenFile(track.audio_file.path)
                if audio.info.length:
                    seconds = int(audio.info.length)
                    track.duration = timedelta(seconds=seconds)
                    track.save(update_fields=["duration"])
            except Exception as e:
                print(f"Error extracting duration: {e}")

        return track    
        
    