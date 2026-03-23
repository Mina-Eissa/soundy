from rest_framework import serializers
from api.models import Stream,Member,Track
from ..serializers import MemberMiniSerializer, TrackSerializer
class StreamSerializer(serializers.ModelSerializer):
    member = MemberMiniSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        queryset = Member.objects.all(),
        source = 'member',
        write_only = True
    )
    track_id = serializers.PrimaryKeyRelatedField(
        queryset = Track.objects.all(),
        source = 'track',
        write_only= True
    )
    started_at=serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Stream
        fields = '__all__'