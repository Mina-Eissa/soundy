import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Member  # or your custom model

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # no auth → continue (DRF will mark as unauthenticated)

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                return None
        except ValueError:
            raise AuthenticationFailed("Invalid authorization header format")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        try:
            user = Member.objects.get(id=payload["user_id"])
        except Member.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, None)  # (user, auth) → user will be available as request.user
