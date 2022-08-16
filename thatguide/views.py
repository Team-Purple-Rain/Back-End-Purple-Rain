from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import generics, permissions
from thatguide.models import HikingCheckPoint, HikingSession, User
from thatguide.serializers import HikeSerializer, UserSerializer
from thatguide.serializers import HikingCheckPointSerializer
from django.shortcuts import get_object_or_404


"""
Home page, get's you a free meme
"""
@api_view(['GET'])
def getMeme(request):
    res = requests.get('https://meme-api.herokuapp.com/gimme')
    data = res.json()

    return Response({
        'team': 'Team Purple Rain',
        'description': 'We are going to crush this project!',
        'meme_image': data['url']
        })


"""
POST /map/ - start hiking session
"""
class HikingSessionView(generics.CreateAPIView):
    queryset = HikingSession.objects.all()
    serializer_class = HikeSerializer


"""
GET /map/<int:pk/ - view hiking session
PATCH /map/<int:pk/ - edit hiking session
"""
class HikingSessionViewList(generics.RetrieveUpdateDestroyAPIView):
    queryset = HikingSession.objects.all()
    serializer_class = HikeSerializer


"""
GET /map/<int:pk>/<checkpoint_pk>/' - view updated location
"""
class HikingCheckPointView(generics.ListCreateAPIView):
    queryset = HikingCheckPoint.objects.all()
    serializer_class = HikingCheckPointSerializer

    def get_queryset(self):
        return HikingCheckPoint.objects.filter(id=self.kwargs["checkpoint_pk"])


"""
POST /map/<int:pk>/checkpoint/' - post updated location
"""
class HikingCheckPointPostView(generics.ListCreateAPIView):
    queryset = HikingCheckPoint.objects.all()
    serializer_class = HikingCheckPointSerializer


"""
GET /users/ - display all users
"""
class UserProfileView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
GET /users/me/ - show your logged in profile
PATCH /users/me/ - update your profile
"""
class UserEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj