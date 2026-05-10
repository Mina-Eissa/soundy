from rest_framework import serializers 
from ..models import Playlist, Track,Member
from .TrackSerializer import TrackSerializer
from .MemberProfileSerializer import MemberProfileSerializer

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','username','is_superuser']

class PlaylistWritingSerializer(serializers.ModelSerializer):
    owner = MemberProfileSerializer(read_only=True)

    # Read full track objects
    tracks = TrackSerializer(read_only=True, many=True)

    # Write using track IDs
    track_ids = serializers.PrimaryKeyRelatedField(
        queryset=Track.objects.all(),
        many=True,
        write_only=True,
        source="tracks",
        required=False,
    )

    cover = serializers.ImageField(required=False)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "name",
            "owner",
            "description",
            "cover",
            "tracks",
            "track_ids",
            "is_public",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        tracks = validated_data.pop("tracks", [])

        playlist = Playlist.objects.create(**validated_data)

        if tracks:
            playlist.tracks.set(tracks)

        return playlist

    def update(self, instance, validated_data):
        tracks = validated_data.pop("tracks", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tracks is not None:
            instance.tracks.set(tracks)

        return instance
