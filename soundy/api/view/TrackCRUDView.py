from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..auth import JWTAuthentication
from ..models import Track
from ..serializers import TrackSerializer
from api.view.FilterQueryMixin import FilterQueryMixin
from django.db.models import Count

class TrackViewSet(FilterQueryMixin,viewsets.ModelViewSet):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)
    def get_queryset(self):
        filters = {
            'artist__id': self.request.query_params.get('member_id'),
            'genre__iexact': self.request.query_params.get('genre'),
        }
        queryset = Track.objects.annotate(
        plays_count=Count('plays', distinct=True),
        reacts_count=Count('reactions', distinct=True),
        comments_count=Count('comments', distinct=True),
        )
        return queryset