from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import generics
from thatguide.models import HikingSession, User
from thatguide.serializers import HikeSerializer, UserSerializer


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
GET /user/ - display user profile
POST /user/ - create user profile
"""
class UserProfileView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer