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

class StreamPlayView(APIView, AudioStreamMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Your JWT
    
    def get(self, request, stream_id):
        """
            Handle GET for streaming audio. Supports 'position' query param for seeking.
        """
        # Get stream session (optional tracking)
        stream = self.get_or_create_stream(request, stream_id)
        if stream:
            track = stream.track
            track_duration = track.duration.total_seconds()
            
        # Parse position (seek support)
        if request.query_params.get('position'):
            position = float(request.query_params.get('position', 0.0))
        else:
            position = stream.last_position
        position = max(0.0, min(position, track_duration))  # Clamp
        
        # Calculate chunk bytes
        track_path = track.audio_file.path
        start_byte = self.position_to_byte(track_path, position, track_duration)
        bytes_per_second = os.path.getsize(track_path) / track_duration
        actual_chunk_duration = min(self.CHUNK_DURATION, track_duration - position)
        end_byte = int(math.ceil((position + actual_chunk_duration) * bytes_per_second))
        
        # Update stream position & time spent
        self.update_stream_position(stream, position+actual_chunk_duration,track_duration)
        self.update_stream_time_spent(stream, actual_chunk_duration)
        
        
        # Metadata for frontend
        metadata = {
            'track_id': track.id,
            'duration': track_duration,
            'position': position,
            'stream_id': stream.id if stream else None
        }
        
        # Stream response
        return self.stream_audio_response(track_path, start_byte, end_byte, metadata)
    
class StreamGetOrCreateView(APIView, AudioStreamMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        """
            Handle POST to create/get stream session for a track. Expects 'member_id' and 'track_id' in body.
        """
        member_id = request.data.get('member_id')
        track_id = request.data.get('track_id')
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)
        
        stream = self.get_or_create_stream(request,member=member, track=track)
        return Response({
            'stream_id': stream.id,
            'track': TrackSerializer(track).data
        })