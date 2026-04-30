from rest_framework import serializers
from .MemberMiniSerializer import MemberMiniSerializer
from .TrackSerializer import TrackSerializer
from ..models import Member,Track,React
class ReactSerializer(serializers.ModelSerializer):
    member = MemberMiniSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    created_at=serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = React
        fields = '__all__'
        
    