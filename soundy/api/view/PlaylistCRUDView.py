from django.db.models import Q, Prefetch, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.auth import JWTAuthentication
from api.permissions import IsPlaylistOwnerOrReadOnly
from api.models import Track,Playlist
from api.serializers import PlaylistReadingSerializer,PlaylistWritingSerializer
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsPlaylistOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):

        tracks_queryset = Track.objects.select_related(
            "artist"
        ).annotate(
            plays_count=Count("plays", distinct=True),
            reacts_count=Count("reactions", distinct=True),
            comments_count=Count("comments", distinct=True)
        )

        queryset = Playlist.objects.select_related(
            "owner"
        ).prefetch_related(
            Prefetch("tracks", queryset=tracks_queryset)
        )

        user = self.request.user

        # Base visibility rules
        if user.is_authenticated:
            queryset = queryset.filter(
                Q(is_public=True) | Q(owner=user)
            )
        else:
            queryset = queryset.filter(is_public=True)

        # Optional request filter
        is_public = self.request.query_params.get("is_public")

        if is_public is not None:

            if is_public.lower() == "true":
                queryset = queryset.filter(is_public=True)

            elif is_public.lower() == "false":

                # only owner can access private playlists
                if user.is_authenticated:
                    queryset = queryset.filter(
                        is_public=False,
                        owner=user
                    )
                else:
                    queryset = queryset.none()

        return queryset.distinct()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update','partial_update']:
            return PlaylistWritingSerializer 
        return PlaylistReadingSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)