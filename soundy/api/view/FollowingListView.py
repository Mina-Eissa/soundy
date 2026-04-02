from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Follow, Member
from api.auth import JWTAuthentication

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Get a list of members that the authenticated user is following.
        """
        member = request.user
        following = Follow.objects.filter(follower=member).select_related('following')
        following_count = following.count()
        following_data = [{'id': f.following.id, 'username': f.following.username} for f in following]
        return Response({'following': following_data, 'count': following_count}, status=200)