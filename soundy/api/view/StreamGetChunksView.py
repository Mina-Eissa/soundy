import os
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from api.models import Stream,Play
from api.auth import JWTAuthentication
from rest_framework.response import Response

class StreamChunkView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    CHUNK_SIZE = 1024 * 1024  # 1MB

    def get(self, request,stream_id):

        if not stream_id:
            return Response({"error": "stream_id required"}, status=400)

        try:
            stream = Stream.objects.select_related("track").get(
                id=stream_id,
                member=request.user
            )
        except Stream.DoesNotExist:
            return Response({"error": "Stream not found"}, status=404)

        track = stream.track
        file_path = track.audio_file.path

        if not os.path.exists(file_path):
            return Response({"error": "File not found"}, status=404)

        file_size = os.path.getsize(file_path)

        # =========================
        #  RANGE (streaming)
        # =========================
        range_header = request.headers.get("Range", "bytes=0-")
        bytes_range = range_header.replace("bytes=", "").split("-")

        start = int(bytes_range[0]) if bytes_range[0] else 0
        end = start + self.CHUNK_SIZE - 1
        end = min(end, file_size - 1)

        length = end - start + 1

        with open(file_path, "rb") as f:
            f.seek(start)
            data = f.read(length)

        response = HttpResponse(data, status=206, content_type="audio/mpeg")
        response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response["Accept-Ranges"] = "bytes"
        response["Content-Length"] = str(length)

        # =========================
        #  POSITION (tracking)
        # =========================
        position_header = request.headers.get("X-Position")

        try:
            current_position = float(position_header) if position_header else stream.last_position
        except ValueError:
            current_position = stream.last_position

        track_duration = track.duration.total_seconds()
        current_position = max(0.0, min(current_position, track_duration))

        self.update_stream_logic(stream, current_position)

        return response
    
    def update_stream_logic(self, stream, current_position):
        last_position = stream.last_position or 0.0

        delta = current_position - last_position

        # ignore invalid movement (seek / rewind / jump)
        if delta < 0 or delta > 10:
            delta = 0

        stream.time_spent += delta
        stream.last_position = current_position

        stream.save(update_fields=["time_spent", "last_position"])

        #  Play logic
        if stream.time_spent >= 30 and not stream.is_counted:
            Play.objects.create(
                member=stream.member,
                track=stream.track
            )
            stream.is_counted = True
            stream.save(update_fields=["is_counted"])
        


