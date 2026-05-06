# views.py
import math
import os
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Track,Member
from api.view.AudioStreamMixin import AudioStreamMixin
from api.serializers import TrackSerializer
from api.auth import JWTAuthentication
from django.http import HttpResponse

class StreamPlayView(APIView, AudioStreamMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Your JWT
    
    def get(self, request, stream_id):
        """
        Audio streaming using HTTP Range (byte-based streaming).
        """

        stream = self.get_or_create_stream(request, stream_id)
        if not stream:
            return Response({"error": "Stream not found"}, status=404)

        track = stream.track
        file_path = track.audio_file.path

        if not os.path.exists(file_path):
            return Response({"error": "File not found"}, status=404)

        file_size = os.path.getsize(file_path)

        range_header = request.headers.get("Range")
        if not range_header:
            range_header = "bytes=0-"

        bytes_range = range_header.replace("bytes=", "").split("-")

        start = int(bytes_range[0]) if bytes_range[0] else 0
        end = int(bytes_range[1]) if len(bytes_range) > 1 and bytes_range[1] else file_size - 1

        start = max(0, start)
        end = min(end, file_size - 1)

        length = end - start + 1

        with open(file_path, "rb") as f:
            f.seek(start)
            data = f.read(length)

        response = HttpResponse(data, status=206, content_type="audio/mpeg")

        response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response["Accept-Ranges"] = "bytes"
        response["Content-Length"] = str(length)

        return response
class StreamGetOrCreateView(APIView, AudioStreamMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        """
            Handle POST to create/get stream session for a track. Expects 'member_id' and 'track_id' in body.
        """
        member = request.user
        track_id = request.data.get('track_id')
        
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)
        
        stream = self.get_or_create_stream(request,member=member, track=track)
        return Response({
            'stream_id': stream.id,
            'track': TrackSerializer(track).data
        })