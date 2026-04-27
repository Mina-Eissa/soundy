from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password
from ..models import Member
from api.auth import JWTAuthentication
from ..serializers import MemberSignInSerializer
class MemberSignInView(APIView):
    
    def post(self, request, *args, **kwargs):
        mem_email = request.data.get("email")
        mem_password = request.data.get("password")
        try:
            instance = Member.objects.filter(email=mem_email).first()
            if not check_password(mem_password ,instance.password):
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = MemberSignInSerializer(instance)
            token = JWTAuthentication().generate_jwt(instance)
            return Response({
                'token': str(token),
                'member': serializer.data,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
