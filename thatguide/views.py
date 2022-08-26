from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from rest_framework import generics, permissions
#from thatguide import serializers
from thatguide.models import HikingCheckPoint, HikingSession, User
from thatguide.serializers import HikeSerializer, UserSerializer
from thatguide.serializers import HikingCheckPointSerializer
from thatguide.serializers import BulkCheckPointSerializer
from math import radians, cos, sin, asin, sqrt
#from django.db.models import F
#from django.shortcuts import get_object_or_404
from decimal import Decimal
#from thatguide.rest import CreateBulkMixin


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


def calc_elevation(new_elevation, this_elevation):
    print(new_elevation)
    elevation1 = new_elevation
    elevation2 = this_elevation
    return (elevation1 - elevation2)


def calcu_elevation(c_elevation, this_elevation):
    elevation1 = c_elevation
    elevation2 = this_elevation
    return (elevation1 - elevation2)


"""
GET /map/ - view hiking session (logged in)
POST /map/ - start hiking session (logged in)
"""
class HikingSessionView(generics.ListCreateAPIView):
    queryset = HikingSession.objects.all()
    serializer_class = HikeSerializer

    def perform_create(self, serializer):
        hike_user = self.request.user
        if hike_user.id is not None:
            serializer.save(hike_user=self.request.user)
        else:
            serializer.save()


"""
GET /map/ - view user's hikes
"""
class UserHikingSessionView(generics.ListAPIView):
    queryset = HikingSession.objects.all()
    serializer_class = HikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = HikingSession.objects.all().filter(hike_user=self.request.user)
        # obj = queryset.get(pk=self.request.user.id)
        # self.check_object_permissions(self.request, obj)
        return queryset


"""
GET /map/<int:pk>/<checkpoint_pk>/' - view updated location
"""
class HikingCheckPointView(generics.ListCreateAPIView):
    queryset = HikingCheckPoint.objects.all()
    serializer_class = HikingCheckPointSerializer

    def get_queryset(self):
        return HikingCheckPoint.objects.filter(id=self.kwargs["checkpoint_pk"])

"""
GET /map/<int:pk/ - view hiking session
PATCH /map/<int:pk/ - edit hiking session
"""
class HikingSessionViewList(generics.RetrieveUpdateDestroyAPIView):
    queryset = HikingSession.objects.all()
    serializer_class = HikeSerializer



"""
POST /map/<int:pk>/checkpoint/' - post updated location
"""
class HikingCheckPointPostView(generics.ListCreateAPIView):
    queryset = HikingCheckPoint.objects.all()
    serializer_class = HikingCheckPointSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        hiking_session = HikingSession.objects.get(pk=request.data['hike_session'])
        hiking_session.current_elevation
        this_elevation = hiking_session.current_elevation
        current_location = hiking_session.start_location
        this_location = current_location
        current_distance = hiking_session.distance_traveled
        if current_distance is not None:
            qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:2]
            cord1, cord2 = [cp.location for cp in qs]
            new_elevation, this_elevation = [cpl.elevation for cpl in qs]
            print('line 136', new_elevation, this_elevation)

            HikingSession.objects.filter(pk=request.data['hike_session']).update(distance_traveled=Decimal(get_distance(cord1, cord2)) + Decimal(current_distance), elevation_gain=calc_elevation(new_elevation, this_elevation))
            return response

        if current_distance is None:
            qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:1]
            get_location = qs.values('location')
            for current in get_location:
                current_spot = current['location']
            new_elevation = qs.values('elevation')
            for e in new_elevation:
                c_elevation = e['elevation']
            print(c_elevation)

            cord2 = current_spot
            cord1 = this_location

            HikingSession.objects.filter(pk=request.data['hike_session']).update(distance_traveled=get_distance(cord1, cord2), elevation_gain=calcu_elevation(c_elevation, this_elevation))
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


"""
POST /map/<int:pk>/bulk/ - post bulk checkpoint data
"""
class BulkViewSet(generics.CreateAPIView):
    queryset = HikingCheckPoint.objects.all()
    serializer_class = BulkCheckPointSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        print("hey, I hate this code")
        return super().get_serializer(*args, **kwargs)
        
    
    # def get_queryset(self, **kwargs):
    #     qs = HikingCheckPoint.objects.filter(hike_session__pk=kwargs['pk'])
    #     print('line 198***', qs)
    #     return qs

    # def create(self, request, *args, **kwargs):
    #     #kwargs['many'] = True
    #     print('line 202***', self, request, args, kwargs)
    #     response = super().create(request)
    #     print('line 204', response)
    #     print("line******", HikingSession.objects.get(kwargs=request.data()))
    #     hiking_session = HikingSession.objects.get(pk=request.data['hike_session'])
    #     print('line 206', hiking_session)
    #     hiking_session.current_elevation
    #     #print(hiking_session.current_elevation)
    #     this_elevation = hiking_session.current_elevation
    #     print('line 210', this_elevation)
    #     current_location = hiking_session.start_location
    #     #print(current_location)
    #     this_location = current_location
    #     #print(this_location)
    #     current_distance = hiking_session.distance_traveled
    #     #print(current_distance)
    #     ###checkpoint = sorted, takes list or iterable, 2nd argument is for sorting.  sort by field that the frton end is passing. ####
    #     for info in response:
    #         #sorted = info
    #         print('line 220', info)

    #         #current_distance = data['current_distance']
    #         if current_distance is not None:
    #             qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:2]
    #             cord1, cord2 = [cp.location for cp in qs]
    #             new_elevation, this_elevation = [cpl.elevation for cpl in qs]
    #             #print(new_elevation)

    #             HikingSession.objects.filter(pk=request.data['hike_session']).update(distance_traveled=Decimal(get_distance(cord1, cord2)) + Decimal(current_distance), elevation_gain=calc_elevation(new_elevation, this_elevation))
    #             return response
            
    #         if current_distance is None:
    #             qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:1]
    #             get_location = qs.values('location')
    #             for current in get_location:
    #                 current_spot = current['location']
    #             new_elevation = qs.values('elevation')
    #             for e in new_elevation:
    #                 c_elevation = e['elevation']
    #             print(c_elevation)

    #             cord2 = current_spot
    #             cord1 = this_location

    #             HikingSession.objects.filter(pk=request.data['hike_session']).update(distance_traveled=get_distance(cord1, cord2), elevation_gain=calc_elevation(c_elevation, this_elevation))
    #             return response