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
    path('', include(member_router.urls)),
    path('',include(track_router.urls)),
    path('', include(playlist_router.urls)),
    path('signin/',MemberSignInView.as_view(),name='member_signin'),
    path('signup/',MemberSignUpView.as_view(),name='member_signup'),
    # JWT endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]