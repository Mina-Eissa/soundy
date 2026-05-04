from rest_framework import serializers
from api.models import Member,Follow

class MemberProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    personal_img = serializers.SerializerMethodField()
    wallpaper_img = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ["id","username","bio","personal_img","wallpaper_img","followers","following"]
    def get_personal_img(self, obj):
        request = self.context.get("request")
        if obj.personal_img:
            url = obj.personal_img.url
            return request.build_absolute_uri(url) if request else url
        return None
    def get_wallpaper_img(self, obj):
        request = self.context.get("request")
        if obj.wallpaper_img:
            url = obj.wallpaper_img.url
            return request.build_absolute_uri(url) if request else url
        return None
    def get_followers(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following(self, obj):
        return Follow.objects.filter(follower=obj).count()