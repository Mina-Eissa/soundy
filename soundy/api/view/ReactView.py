from rest_framework import generics, request,serializers
from ..serializers import ReactSerializer
from rest_framework.permissions import IsAuthenticated
from ..auth import JWTAuthentication
from ..models import React,Member,Track
from rest_framework.response import Response
from rest_framework import status
class ReactView( generics.ListCreateAPIView
                ,generics.DestroyAPIView
                ,generics.RetrieveAPIView):
    queryset = React.objects.all()
    serializer_class = ReactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        track_id = self.kwargs.get('track_id')
        track = generics.get_object_or_404(Track, id=track_id)
        serializer.save(member=self.request.user, track=track)
        
    def list(self, request, *args, **kwargs):
        track_id = self.kwargs.get("track_id")

        if not track_id:
            return Response(
                {"error": "track_id is required"},
                status=400
            )
        track = generics.get_object_or_404(Track, id=track_id)
        user = request.user
        reactions = React.objects.filter(track=track)
        liked = False
        
        if user.is_authenticated:
            reactForMember = reactions.filter(member=user).first()
            if reactForMember:
                liked = True
        serializer = self.get_serializer(reactions, many=True)

        return Response({
                "liked": liked,
                "reacts": serializer.data,
                "count": reactions.count(),
                "myReactId": reactForMember.member.id if liked else None
            
        })
    def retrieve(self, request, *args, **kwargs):
        user = request.user

        track = self.get_object()

        reactions = React.objects.filter(track=track).select_related("member")

        liked = False
        if user.is_authenticated:
            reactForMember = reactions.filter(member=user).first()
            if reactForMember:
                liked = True

        serializer = ReactSerializer(reactions, many=True)

        return Response({
            "liked": liked,
            "reacts": serializer.data,
            "count": reactions.count(),
            "myReactId": reactForMember.member.id if liked else None
        })
        
    def destroy(self, request, *args, **kwargs):
        track_id = self.kwargs.get('track_id')
        if not track_id:
            return Response(
                {"error": "track_id is required"},
                status=400
            )
        track = generics.get_object_or_404(Track, id=track_id)
        user = request.user
        reactions = React.objects.filter(track=track)
        liked = False
        
        if user.is_authenticated:
            React.objects.filter(
            track=track,
            member=request.user
            ).delete()
        
        serializer = self.get_serializer(reactions, many=True)

        return Response({
                "liked": liked,
                "reacts": serializer.data,
                "count": reactions.count(),            
        })
        