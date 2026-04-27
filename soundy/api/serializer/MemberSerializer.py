from rest_framework import serializers
from ..models import Member
from django.contrib.auth.hashers import make_password
class MemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    password = serializers.CharField(write_only=True)
    birth_date=serializers.DateField(required=True,format="%Y-%m-%d",input_formats=['%Y-%m-%d','%d-%m-%Y','%d/%m/%Y'])
    created_at=serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model= Member
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)