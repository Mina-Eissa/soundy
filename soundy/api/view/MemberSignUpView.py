from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Member
from ..serializers import MemberSerializer
from api.auth import JWTAuthentication
class MemberSignUpView(CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        # mem_password = request.data.get("password")
        # request.data["password"] = make_password(mem_password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = JWTAuthentication().generate_jwt(serializer.instance)
        return Response({'token':str(token),
                        'member':serializer.data}, status=status.HTTP_201_CREATED)