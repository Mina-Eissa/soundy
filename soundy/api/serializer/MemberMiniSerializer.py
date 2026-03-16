from rest_framework import serializers
from ..models import Member

class MemberMiniSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)

    class Meta:
        model= Member
        fields = ['id','username']