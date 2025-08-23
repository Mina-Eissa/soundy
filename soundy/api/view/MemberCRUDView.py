from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Member
from ..serializers import MemberSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        refresh = RefreshToken.for_user(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response({'refresh_token':str(refresh),
                         'access_token':str(refresh.access_token),
                         'member':serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        refresh = RefreshToken.for_user(instance)
        return Response({'refresh_token':str(refresh),
                         'access_token':str(refresh.access_token),
                         'member':serializer.data})