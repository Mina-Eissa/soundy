from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Stream, Track, Member
from api.auth import JWTAuthentication

class StreamInitView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        track_id = request.data.get("track_id")
        if not track_id:
            return Response({"error": "track_id required"}, status=400)

        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({"error": "Track not found"}, status=404)

        stream, _ = Stream.objects.get_or_create(
            member=request.user,
            track=track,
        )

        return Response({
            "stream_id": stream.id,
            "last_position": stream.last_position,
            "duration": track.duration.total_seconds()
        })