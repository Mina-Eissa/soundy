from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import PlaylistReadingSerializer,PlaylistwritingSerializer
from ..models import Playlist
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_serializer_class(self):
        if self.action in ['create', 'update','partial_update']:
            return PlaylistwritingSerializer
        return PlaylistReadingSerializer