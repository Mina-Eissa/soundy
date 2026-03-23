import os
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.models import Member,Track,Stream
from api.serializers import StreamSerializer
from rest_framework.response import Response
from api.streamfuctions import get_audio_chunk, calculate_next_position,stream_audio_chunk
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from api.view.AudioStreamMixin import AudioStreamMixin
from api.auth import JWTAuthentication

class StreamStartView(APIView, AudioStreamMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = StreamSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        member = serializer.validated_data['member']
        track = serializer.validated_data['track']
        
        try:
            
            # Create or get active stream
            stream, created = Stream.objects.get_or_create(
                member=member,
                track=track,
                defaults={'last_position': 0}
            )
            stream.is_active = True
            
            # Calculate chunk range (first 10 seconds or first MB)
            track_path = track.audio_file.path
            duration = track.duration.total_seconds()
            chunk_duration = min(10.0, duration)  # First 10 seconds or full track
            start_byte = 0
            bytes_per_second = os.path.getsize(track_path) / duration if duration > 0 else 0
            end_byte = int(chunk_duration * bytes_per_second)
            
            # Update last position
            stream.last_position = chunk_duration
            stream.save()
            
            def stream_audio():
                yield b'HTTP/1.1 200 OK\r\n'
                yield b'Content-Type: audio/mpeg\r\n'
                yield f'Content-Range: bytes {start_byte}-{end_byte-1}/{os.path.getsize(track_path)}\r\n'.encode()
                yield b'\r\n'
                for chunk in self.get_audio_chunk(track_path, start_byte, end_byte):
                    yield chunk
            
            response = StreamingHttpResponse(
                streaming_content=stream_audio(),
                content_type='audio/mpeg'
            )
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = end_byte - start_byte
            
            return response
            
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        except Track.DoesNotExist:
            return Response({"error": "Track not found"}, status=status.HTTP_404_NOT_FOUND)
