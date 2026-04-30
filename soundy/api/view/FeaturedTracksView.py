"""
This api should return the most popular tracks in the last 24 hours, based on the number of streams and reactions.
The tracks should be ordered by popularity, with the most popular track appearing first.
Each track should include its title, artist, album, genre, and a link to the track's page on the Soundy website.
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models import *
from api.serializers import TrackSerializer

class FeaturedTracksView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        last_24h = timezone.now() - timedelta(hours=24)

        # 🔥 Top 5 in last 24h
        top_24h = (
            Track.objects.annotate(
                plays_count=Count("plays", filter=Q(plays__timestamp__gte=last_24h)),
                reacts_count=Count("reactions", filter=Q(reactions__created_at__gte=last_24h)),
                comments_count=Count("comments", filter=Q(comments__created_at__gte=last_24h)),
            )
            .order_by("-plays_count", "-reacts_count", "-comments_count")
        )[:5]

        # 🔥 Remaining tracks (all-time)
        remaining = (
            Track.objects.exclude(id__in=top_24h.values_list("id", flat=True))
            .annotate(
                plays_count=Count("plays"),
                reacts_count=Count("reactions"),
                comments_count=Count("comments"),
            )
            .order_by("-plays_count", "-reacts_count", "-comments_count")
        )

        # 🔥 Combine results
        final_tracks = list(top_24h) + list(remaining)

        serializer = TrackSerializer(final_tracks, many=True,context={"request": request})
        return Response(serializer.data)