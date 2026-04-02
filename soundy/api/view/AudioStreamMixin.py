# mixins.py
import os
from django.http import StreamingHttpResponse
from django.contrib.auth.models import AnonymousUser,AbstractUser
from api.models import Stream, Track

class AudioStreamMixin:
    CHUNK_DURATION = 10.0  # seconds per chunk
    CHUNK_SIZE = 1024 * 1024  # 1MB
    
    def get_or_create_stream(self, request,stream_id=None,member=None, track=None):
        """Get or create stream session for user+track"""
        print(member)
        if stream_id:
            stream = Stream.objects.get(id=stream_id)
            return stream
        try:
            stream, created = Stream.objects.get_or_create(
                member=member, 
                track=track,
            )
            return stream
        except Exception as e:
            print(f"Error creating stream: {e}")
    
    def update_stream_position(self, stream, position,track_duration):
        """Update stream last_position"""
        if stream:
            stream.last_position = ( position if position < track_duration else 0)
            stream.save(update_fields=['last_position'])
    def update_stream_time_spent(self, stream, time_spent):
        """Update stream time_spent"""
        if stream:
            stream.time_spent += time_spent
            stream.save(update_fields=['time_spent'])
            if stream.time_spent >= 30 and stream.is_counted == False:
                stream.track.plays += 1
                stream.is_counted = True
                stream.save(update_fields=['is_counted'])
                stream.track.save(update_fields=['plays'])
    
    def position_to_byte(self, track_path, position, duration):
        """Convert seconds → bytes"""
        file_size = os.path.getsize(track_path)
        bytes_per_second = file_size / duration if duration > 0 else 0
        return int(position * bytes_per_second)
    
    def get_audio_chunk(self, track_path, start_byte, end_byte):
        """Generator: yield exact byte range"""
        file_size = os.path.getsize(track_path)
        end_byte = min(end_byte or file_size, file_size)
        
        with open(track_path, 'rb') as f:
            f.seek(start_byte)
            remaining = end_byte - start_byte
            
            while remaining > 0:
                chunk_size = min(self.CHUNK_SIZE, remaining)
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)
    
    def stream_audio_response(self, track_path, start_byte, end_byte, metadata=None):
        """Create streaming response with headers"""
        file_size = os.path.getsize(track_path)
        
        def generate():
            if metadata:
                yield f'METADATA:{metadata}\n'.encode()
            yield from self.get_audio_chunk(track_path, start_byte, end_byte)
        
        response = StreamingHttpResponse(
            generate(),
            content_type='audio/mpeg'
        )
        
        response['Accept-Ranges'] = 'bytes'
        response['Content-Range'] = f'bytes {start_byte}-{end_byte-1}/{file_size}'
        response['Content-Length'] = end_byte - start_byte
        return response