from rest_framework import generics
from ..serializers import CommentSerializer
from ..models import Comment,Member,Track
from rest_framework.permissions import IsAuthenticated
from ..auth import JWTAuthentication

class CommentView(generics.ListCreateAPIView,
                  generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

