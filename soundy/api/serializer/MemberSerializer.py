from rest_framework import serializers
from ..models import Member

class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.UUIDField(read_only = True)
    birth_date=serializers.DateField(required=True)

    class Meta:
        model= Member
        fields = '__all__'