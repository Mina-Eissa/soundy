from rest_framework import serializers
from ..models import Track,Member
from ..serializers import MemberMiniSerializer

from mutagen import File as MutagenFile
from datetime import timedelta
import os

class TrackSerializer(serializers.ModelSerializer):
    # Show nested artist details (read-only)
    artist = MemberMiniSerializer(read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)
    plays = serializers.SerializerMethodField()
    reacts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    published_at=serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    cover = serializers.SerializerMethodField()

    
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ["duration"]
        
        
    def get_plays(self, obj):
        return getattr(obj, "plays_count", 0)
    def get_reacts(self,obj):
        return getattr(obj, "reacts_count", 0)
    def get_comments(self,obj):
        return getattr(obj, "comments_count", 0)
    def get_duration(self, obj):
        return obj.duration.total_seconds() if obj.duration else 0
    def get_cover(self, obj):
        request = self.context.get("request")
        if obj.cover:
            url = obj.cover.url
            if request:
                return request.build_absolute_uri(url)
            else:
                return url
        return None
    
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
        
    