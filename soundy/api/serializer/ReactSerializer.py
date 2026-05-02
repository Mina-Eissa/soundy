from rest_framework import serializers
from .MemberMiniSerializer import MemberMiniSerializer
from .TrackSerializer import TrackSerializer
from ..models import Member,Track,React
class ReactSerializer(serializers.ModelSerializer):
    userid = serializers.UUIDField(source="member.id", read_only=True)
    username = serializers.CharField(source="member.username", read_only=True)
    userimage = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = React
        fields = ["id","userid","username","userimage","reaction","created_at"]
    
    def get_userimage(self, obj):
        request = self.context.get("request")
        if obj.member and obj.member.personal_img:
            url = obj.member.personal_img.url
            return request.build_absolute_uri(url) if request else url
        return None