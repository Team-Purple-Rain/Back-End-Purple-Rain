from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import generics, permissions
from thatguide.models import HikingCheckPoint, HikingSession, User
from thatguide.serializers import HikeSerializer, UserSerializer
from thatguide.serializers import HikingCheckPointSerializer
from math import radians, cos, sin, asin, sqrt


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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:2]
        cord1, cord2 = [cp.location for cp in qs]

        def get_distance(cord1, cord2):

            # The math module contains a function named
            # radians which converts from degrees to radians.
            lon1 = radians(cord1['longitude'])
            lon2 = radians(cord2['longitude'])
            lat1 = radians(cord1['latitude'])
            lat2 = radians(cord2['latitude'])

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

            c = 2 * asin(sqrt(a))

            # Radius of earth in miles
            r = 3956

            # calculate the result
            return (c * r)
        HikingSession.objects.filter(pk=request.data['hike_session']).update(distance_traveled=get_distance(cord1, cord2))
        return response

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

