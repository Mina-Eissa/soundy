from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Follow, Member
from api.auth import JWTAuthentication  

class FollowCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def post(self, request):
        """
        Follow a member.
        Expects 'followed_id' in the request data.
        """
        follower = request.user
        followed_id = request.data.get('followed_id')
        if followed_id == str(follower.id):
            return Response({'error': 'You cannot follow yourself.'}, status=400)
        
        if not followed_id:
            return Response({'error': 'followed_id is required.'}, status=400)

        try:
            followed = Member.objects.get(id=followed_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member to follow does not exist.'}, status=404)

        if Follow.objects.filter(follower=follower, following=followed).exists():
            return Response({'error': 'You are already following this member.'}, status=400)

        Follow.objects.create(follower=follower, following=followed)
        return Response({'message': f'You are now following {followed.username}.'}, status=201)