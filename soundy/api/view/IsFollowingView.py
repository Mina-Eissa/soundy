from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.auth import JWTAuthentication
from api.models import Follow, Member

class IsFollowingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, member_id):
        """
        Check if the authenticated user is following the member with the given ID.
        """
        follower = request.user
        followed_id = member_id
        try:
            followed = Member.objects.get(id=followed_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist.'}, status=404)

        is_following = Follow.objects.filter(follower=follower, following=followed).exists()
        return Response({'is_following': is_following}, status=200)