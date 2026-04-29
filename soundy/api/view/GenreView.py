from rest_framework.views import APIView
from rest_framework.response import Response
from api.model.Track import Genre
from api.auth import JWTAuthentication
from rest_framework.permissions import IsAuthenticated 

class GenreListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response([
            {"value": g.value, "label": g.label}
            for g in Genre
        ])