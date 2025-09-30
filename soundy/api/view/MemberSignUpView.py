from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Member
from ..serializers import MemberSerializer
from ..independent_func import generate_jwt

class MemberSignUpView(CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        request.data["password"] = make_password(request.data.get("password"))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = generate_jwt(serializer.instance)
        return Response({'token':str(token),
                        'member':serializer.data}, status=status.HTTP_201_CREATED)