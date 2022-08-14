from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import generics
from thatguide.models import HikingSession
from thatguide.serializers import HikeSerializer


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