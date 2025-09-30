from rest_framework import viewsets,status
from rest_framework.response import Response
from ..models import Member
from ..serializers import MemberSerializer
from ..independent_func import generate_jwt

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = generate_jwt(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response({'token':str(token),
                         'member':serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        token = generate_jwt(serializer.instance)
        return Response({'token':str(token),
                         'member':serializer.data})