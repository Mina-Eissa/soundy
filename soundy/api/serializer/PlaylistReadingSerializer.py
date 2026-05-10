from rest_framework import serializers 
from ..models import Playlist, Track,Member
from .TrackSerializer import TrackSerializer
from .MemberProfileSerializer import MemberProfileSerializer

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','username','is_superuser']

class PlaylistReadingSerializer(serializers.ModelSerializer):
    owner = MemberProfileSerializer(read_only=True)
    tracks = TrackSerializer(many=True,read_only=True)
    createdAt = serializers.DateTimeField(source='created_at',format="%Y-%m-%d %H:%M",read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at',format="%Y-%m-%d %H:%M",read_only=True)

    
    class Meta:
        model = Playlist
        fields = '__all__'
        