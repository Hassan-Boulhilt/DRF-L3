from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets 
from rest_framework import mixins
from profiles.models import Profile, ProfileStatus

from profiles.api.permissions import IsOwneProfileOrReadOnly, IsOwnerOrReadOnly
from profiles.api.serializers import ProfileSerializer, ProfileAvatarSerializer ,ProfileStatusSerializer

class AvatarUpdateView(generics.UpdateAPIView):
    
    serializer_class = ProfileAvatarSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object
    
class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwneProfileOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['city']
    
class ProfileStatusViewSet(ModelViewSet):
    
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = ProfileStatus.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user_profile__user__username=username)
        return queryset
    
    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)