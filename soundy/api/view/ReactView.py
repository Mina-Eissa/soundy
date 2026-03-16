from rest_framework import generics
from ..serializers import ReactSerializer
from rest_framework.permissions import IsAuthenticated
from ..auth import JWTAuthentication
from ..models import React
class ReactView( generics.ListCreateAPIView
                ,generics.DestroyAPIView
                ,generics.RetrieveAPIView):
    queryset = React.objects.all()
    serializer_class = ReactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    