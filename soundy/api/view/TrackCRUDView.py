from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Track
from ..serializers import TrackSerializer


class TrackViewSet(viewsets.ModelViewSet):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]