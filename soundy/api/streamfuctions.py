import os
from django.conf import settings
import math,json
def get_audio_chunk(file_path, start_pos, chunk_duration=10.0):
    """
    Get audio chunk starting from start_pos for chunk_duration seconds
    Returns bytes and actual duration of chunk
    """
    if not os.path.exists(file_path):
        return None, 0
    
    file_size = os.path.getsize(file_path)
    chunk_size = int(math.ceil(file_size * (chunk_duration / 300.0)))  # rough estimation
    
    # Calculate byte range for audio chunk
    start_byte = int(start_pos * (file_size / 300.0))  # assuming ~300s total
    end_byte = min(start_byte + chunk_size, file_size)
    
    with open(file_path, 'rb') as f:
        f.seek(start_byte)
        chunk = f.read(end_byte - start_byte)
    
    actual_duration = min(chunk_duration, (end_byte - start_byte) * 300.0 / file_size)
    return chunk, actual_duration

def calculate_next_position(current_pos, chunk_duration, track_duration):
    """Calculate next position considering track end"""
    return min(current_pos + chunk_duration, track_duration)

def stream_audio_chunk(chunk_data, stream_id, next_position, track_duration):
    """Generator for streaming audio chunk with metadata"""
    # Send metadata first
    metadata = json.dumps({
        'stream_id': str(stream_id),
        'next_position': str(next_position),
        'track_duration': str(track_duration),
        'chunk_size': len(chunk_data)
    }).encode()
    yield metadata + b'\n'  # separator
    yield chunk_data