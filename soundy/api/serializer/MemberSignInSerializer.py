from rest_framework import serializers
from ..models import Member

class MemberSignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,write_only=True)
    password = serializers.CharField(required=True,write_only=True)
    created_at=serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    # personal_img=serializers.ImageField(required=False,allow_null=True)
    class Meta:
        model=Member
        fields=['username','email','password','created_at','personal_img']    