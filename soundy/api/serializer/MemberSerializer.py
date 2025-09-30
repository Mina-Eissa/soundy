from rest_framework import serializers
from ..models import Member

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    password = serializers.CharField(write_only=True)
    birth_date=serializers.DateField(required=True,format="%Y-%m-%d",input_formats=['%Y-%m-%d','%d-%m-%Y','%d/%m/%Y'])

    class Meta:
        model= Member
        fields = '__all__'