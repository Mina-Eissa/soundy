from rest_framework import viewsets,status
from rest_framework.response import Response
from ..models import Member
from ..serializers import MemberSerializer
from ..auth import JWTAuthentication
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.permissions import IsAuthenticated
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "member": serializer.data
        })