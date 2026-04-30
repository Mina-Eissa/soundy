from rest_framework import generics
from ..serializers import CommentSerializer
from ..models import Comment,Member,Track
from rest_framework.permissions import IsAuthenticated
from ..auth import JWTAuthentication
from rest_framework.response import Response

class CommentView(generics.ListCreateAPIView,
                  generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        track_id = self.kwargs.get('track_id')
        track = generics.get_object_or_404(Track, id=track_id)
        serializer.save(member=self.request.user, track=track)
        
    def list(self, request,track_id):
        track = generics.get_object_or_404(Track, id=track_id)
        comments = Comment.objects.filter(track=track)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)