from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Follow, Member
from api.auth import JWTAuthentication


class FollowView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_target(self, member_id):
        try:
            return Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return None

    def get(self, request, member_id):
        """
        Check if current user is following this member
        """
        follower = request.user
        target = self.get_target(member_id)

        if not target:
            return Response({'error': 'Member not found'}, status=404)

        is_following = Follow.objects.filter(
            follower=follower,
            following=target
        ).exists()

        return Response({
            "following": is_following
        }, status=200)

    def post(self, request, member_id):
        """
        Follow a member
        """
        follower = request.user
        target = self.get_target(member_id)

        if not target:
            return Response({'error': 'Member not found'}, status=404)

        if follower.id == target.id:
            return Response({'error': 'You cannot follow yourself'}, status=400)

        if Follow.objects.filter(follower=follower, following=target).exists():
            return Response({'error': 'Already following'}, status=400)

        Follow.objects.create(follower=follower, following=target)

        return Response({
            "message": f"You are now following {target.username}",
            "following": True
        }, status=201)

    def delete(self, request, member_id):
        """
        Unfollow a member
        """
        follower = request.user
        target = self.get_target(member_id)

        if not target:
            return Response({'error': 'Member not found'}, status=404)

        follow = Follow.objects.filter(
            follower=follower,
            following=target
        ).first()

        if not follow:
            return Response({'error': 'You are not following this member'}, status=400)

        follow.delete()

        return Response({
            "message": f"You unfollowed {target.username}",
            "following": False
        }, status=200)