"""
This API should return the most recently added tracks to 
the Soundy platform, ordered by their release date,with the newest tracks appearing first.
Each track should include its title, artist, album, genre, and a link to the track's page on the Soundy website.
"""
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models import *
from api.serializers import TrackSerializer

class RecentTracksView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        recent_tracks = Track.objects.annotate(
            plays_count=Count("plays"),
            reacts_count=Count("reactions"),
            comments_count=Count("comments"),
            ).order_by("-published_at")[:20]  # Get the 20 most recent tracks
        serializer = TrackSerializer(recent_tracks, many=True, context={"request": request})
        return Response(serializer.data)