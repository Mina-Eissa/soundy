from rest_framework import viewsets,status
from rest_framework.response import Response
from ..models import Member
from ..serializers import MemberSerializer
from ..auth import JWTAuthentication
from django.contrib.auth.hashers import make_password,check_password

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def create(self, request, *args, **kwargs):
        mem_password = request.data.get('password')
        if mem_password is None or len(mem_password)<6:
            return Response({'error':'Password must be at least 6 characters long.'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['password'] = make_password(mem_password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = JWTAuthentication().generate_jwt(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response({'token':str(token),
                         'member':serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        mem_password = request.data['password']
        instance = self.get_object()
        if not check_password(mem_password,instance.password):
            return Response({'error':'password wrong'},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        token = JWTAuthentication().generate_jwt(serializer.instance)
        return Response({'token':str(token),
                         'member':serializer.data})