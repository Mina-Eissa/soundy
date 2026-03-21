from rest_framework import serializers
from api.models import Comment
from ..serializers import MemberMiniSerializer, TrackSerializer
from ..models import Member, Track

class CommentSerializer(serializers.ModelSerializer):
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
    created_at=serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Comment
        fields = '__all__'