from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.auth import JWTAuthentication
from api.models import *
from api.serializers import TrackSerializer

class TracksForMember(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        member = request.user
        tracks = Track.objects.filter(artist__id=member.id).annotate(
            plays_count=Count("plays",distinct=True),
            reacts_count=Count("reactions",distinct=True),
            comments_count=Count("comments",distinct=True),
        ).order_by("-published_at")
        serializer = TrackSerializer(tracks, many=True, context={"request": request})
        return Response(serializer.data)