from django.db import router
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import *

member_router = DefaultRouter()
member_router.register(r'member', MemberViewSet)
track_router = DefaultRouter()
track_router.register(r'track',TrackViewSet)
playlist_router = DefaultRouter()
playlist_router.register(r'playlist', PlaylistViewSet)

urlpatterns = [
    path('track/featured/',FeaturedTracksView.as_view(),name='featured-tracks'),
    path('track/recent/',RecentTracksView.as_view(),name='recent-tracks'),
    path('track/genre/',GenreListView.as_view(),name='genre-list'),
    path('track/<uuid:track_id>/comments/',CommentView.as_view(),name='track_member_comment'),
    path('track/<uuid:track_id>/reacts/',ReactView.as_view(),name='track_member_react'),
    path('track/stream/init/',StreamInitView.as_view(),name='stream-create'),
    path('track/stream/<uuid:stream_id>/',StreamChunkView.as_view(),name='stream-play'),
    path('signin/',MemberSignInView.as_view(),name='member_signin'),
    path('signup/',MemberSignUpView.as_view(),name='member_signup'),
    path('member/tracks/',TracksForMember.as_view(),name='tracks-for-member'),
    path('member/<uuid:member_id>/follow/',FollowView.as_view(),name='follow-member'),
    path('', include(member_router.urls)),
    path('',include(track_router.urls)),
    path('', include(playlist_router.urls)),
    path('Following/',FollowingListView.as_view(),name='following-list'),
    path('Followers/',FollowersListView.as_view(),name='followers-list'),
    # JWT endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]