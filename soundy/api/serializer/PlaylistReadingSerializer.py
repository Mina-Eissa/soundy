from rest_framework import serializers 
from ..models import Playlist, Track,Member
from .TrackSerializer import TrackSerializer


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','username','is_superuser']

class PlaylistReadingSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    tracks = TrackSerializer(many=True,read_only=True)
    tracks_count = serializers.SerializerMethodField(read_only=True)
    
    def get_track_count(self,obj):
        return obj.tracks.count()
    
    class Meta:
        model = Playlist
        field = '__all__'
        