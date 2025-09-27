from rest_framework import serializers 
from ..models import Playlist, Track,Member
from .TrackSerializer import TrackSerializer


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','username','is_superuser']

class PlaylistwritingSerializer(serializers.ModelSerializer):
    owner=OwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        source="owner",
        write_only=True
    )
    tracks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Track.objects.all()
    )
    tracks_count = serializers.SerializerMethodField(read_only=True)
    
    def get_tracks_count(self, obj):
        return obj.tracks.count()
    
    class Meta:
        model = Playlist
        fields = '__all__'
