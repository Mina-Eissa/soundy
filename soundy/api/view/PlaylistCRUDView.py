from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.permissions import IsPlaylistOwnerOrReadOnly
from ..auth import JWTAuthentication
from ..serializers import PlaylistReadingSerializer,PlaylistWritingSerializer
from ..models import Playlist,Track
from django.db.models import Prefetch, Count
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.select_related(
        "owner"
        ).prefetch_related(
        Prefetch(
            "tracks",
            queryset=Track.objects.select_related(
                "artist"
            ).annotate(
                plays_count=Count("plays", distinct=True),
                reacts_count=Count("reactions", distinct=True),
                comments_count=Count("comments", distinct=True)
            )
        )
        )
    permission_classes = [IsAuthenticatedOrReadOnly, IsPlaylistOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    def get_serializer_class(self):
        if self.action in ['create', 'update','partial_update']:
            return PlaylistWritingSerializer
        return PlaylistReadingSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)