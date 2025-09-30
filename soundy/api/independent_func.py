

"""
    APIs functions 
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt(user):
    payload = {
        "user_id": str(user.id),
        "exp": datetime.now() + timedelta(hours=24),
        "iat": datetime.now(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
