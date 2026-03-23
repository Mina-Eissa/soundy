import os

class AudioStreamMixin:
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks
    
    def get_audio_chunk(self, track_path, start_byte=0, end_byte=None):
        """Generator to yield audio chunks from file"""
        file_size = os.path.getsize(track_path)
        end_byte = min(end_byte or file_size, file_size)
        
        with open(track_path, 'rb') as audio_file:
            audio_file.seek(start_byte)
            remaining = end_byte - start_byte
            while remaining > 0:
                chunk_size = min(self.CHUNK_SIZE, remaining)
                chunk = audio_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)
    
    def position_to_byte(self, track_path, position_seconds, duration):
        """Convert time position to byte position (rough estimation)"""
        file_size = os.path.getsize(track_path)
        # Rough estimation: bytes per second = file_size / duration
        bytes_per_second = file_size / duration if duration > 0 else 0
        return int(position_seconds * bytes_per_second)