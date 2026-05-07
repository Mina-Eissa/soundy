from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import status
from api.models import Track,Member
from api.model.Track import Genre
from api.validators import validate_query_text
from api.serializers import MemberProfileSerializer, TrackSerializer
from django.db.models import Q, Count

class SearchView(APIView):
    def get(self,request):
        query = request.GET.get("q", "").strip()
        
        # validate query from HTML tags, operations and SQL injection
        validateResponse = validate_query_text(query)
        if isinstance(validateResponse, ValidationError):
            return Response({"error": validateResponse}, status=status.HTTP_400_BAD_REQUEST)
        
        searchQuery = query.lower()
        genres = []

        for value, label in Genre.choices:
            if searchQuery  in label.lower():
                genres.append({
                    "value": value,
                    "label": label
                })
        
        artists = Member.objects.filter(
            username__icontains=query
        )[:10]

        tracks = Track.objects.annotate(  
            plays_count=Count("plays", distinct=True),
            reacts_count=Count("reactions", distinct=True),
            comments_count=Count("comments", distinct=True),
        ).filter(
            Q(name__icontains=query) |
            Q(genre=query)
        ).select_related("artist")[:10]

        return Response({
            "artists": MemberProfileSerializer(artists, many=True).data,
            "genres": genres,
            "tracks": TrackSerializer(tracks, many=True).data,
        })