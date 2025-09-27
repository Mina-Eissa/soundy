from django.core.exceptions import ValidationError
import magic
import re
def validate_name(value):
    pattern = r'^[A-Za-z0-9_\- ]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Member Name can only contain letters, numbers, underscores (_), hyphens (-), and spaces."
        )


def validate_safe_text(value):
    # 1) Prevent HTML tags
    if re.search(r'<[^>]*>', value):
        raise ValidationError("HTML tags are not allowed.")
    # 2) Prevent Operations 
    if re.search(r'^[=;]+', value):
        raise ValidationError("any operations not allowed.")
    # 3) Prevent common SQL injection words
    forbidden_sql = [
        "SELECT", "INSERT", "UPDATE", "DELETE",
        "DROP", "ALTER", "CREATE", "EXEC",
        "UNION", "CAST"
    ]
    for word in forbidden_sql:
        if word.lower() in value.lower():
            raise ValidationError("Invalid input, contains forbidden keywords.")



def validate_audio_mime(value):
    mime = magic.from_buffer(value.read(2048), mime=True)
    value.seek(0)  # reset pointer after reading
    if not mime.startswith("audio/"):
        raise ValidationError("Only audio files are allowed.")

def validate_image_mime(value):
    # Read first bytes of the file to detect type
    mime = magic.from_buffer(value.read(2048), mime=True)
    value.seek(0)  # reset file pointer after reading

    if not mime.startswith("image/"):
        raise ValidationError("Only image files are allowed.")
    
    # Optionally: restrict to specific types
    allowed_mimes = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if mime not in allowed_mimes:
        raise ValidationError("Only JPEG, PNG, GIF, or WEBP images are supported.")
