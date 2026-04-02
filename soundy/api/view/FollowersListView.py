from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Follow, Member   
from api.auth import JWTAuthentication

class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Get a list of followers for the authenticated user.
        """
        member = request.user
        followers = Follow.objects.filter(following=member).select_related('follower')
        followers_count = followers.count()
        followers_data = [{'id': f.follower.id, 'username': f.follower.username} for f in followers]
        return Response({'followers': followers_data, 'count': followers_count}, status=200)