import json
import os
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
#from thatguide import test
#from thatguide.rest import CreateBulkMixin
from django.conf import settings






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


def calc_elevation(new_elevation, old_elevation):
    #print(new_elevation)
    elevation1 = new_elevation
    elevation2 = old_elevation
    return (elevation1 - elevation2)


def calcu_elevation(c_elevation, current_elevation):
    elevation1 = c_elevation
    elevation2 = current_elevation
    return (elevation1 - elevation2)


f = open(os.path.join(settings.BASE_DIR, 'static', 'trail.json'))
data = json.load(f)
coordinates = [{'longitude': long, 'latitude': lat} for long, lat in data['features'][0]['geometry']['coordinates']]
f.close()


"""
GET /map/ - view hiking session 
POST /map/ - start hiking session 
"""
class HikingSessionView(generics.ListCreateAPIView):
    queryset = HikingSession.objects.all()
    serializer_class = HikeSerializer

    def create(self, request, *args, **kwargs):
        if 'end_location' in request.data and request.data['end_location'] is not None:
            distance = 0
            current_cord = None
            next_cord = None
            start_location = request.data['start_location']
            end_location = request.data['end_location']
            closest_distance = 100000
            closest_cord = None

            # calculate distance from users location to coordinates in json file, closest distance is "hop on" spot on trail
            for cord in coordinates:
                distance_to = get_distance(cord, start_location)
                # comparing the distance from each point with closest point so far,
                # find the point with shortest distance and assign variable
                if distance_to < closest_distance:
                    closest_distance = distance_to
                    closest_cord = cord
            
            # loop through file and find accumlation distance from the start and finish point
            for cord in coordinates:

                # calculate the distance from point to point on the list between "hop" on coordinate and end location coordinate
                # add distances together to get total distance to destination
                if current_cord:
                    next_cord = current_cord
                    current_cord = cord
                    distance += get_distance(current_cord, next_cord)

                # looking for "hop on" location point
                elif closest_cord == cord:
                    current_cord = closest_cord

                # if end is found first, swap the end points and continue looping
                elif end_location == cord:
                    current_cord = end_location
                    temp = closest_cord
                    closest_cord = end_location
                    end_location = temp

                # stop loop so that we calculate only the distance between the two points, we don't want distance outside of the coordinates
                if end_location == cord:
                    break


            request.data['distance'] = int(distance + closest_distance)

        response = super().create(request, *args, **kwargs)
        return response

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
        current_elevation = hiking_session.current_elevation
        current_location = hiking_session.start_location
        this_location = current_location
        current_distance = hiking_session.distance_traveled
        elevation_gain = hiking_session.elevation_gain
        elevation_loss = hiking_session.elevation_loss

        if current_distance is not None:
            qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:2]
            cord1, cord2 = [cp.location for cp in qs]
            new_elevation, old_elevation = [cpl.elevation for cpl in qs]
            #print('line 136', new_elevation, this_elevation)
            
            checkpoint_gain = calc_elevation(new_elevation, old_elevation)
            if checkpoint_gain >= 0:
                HikingSession.objects.filter(pk=request.data['hike_session']).update(elevation_gain=checkpoint_gain + elevation_gain)
            else:
                HikingSession.objects.filter(pk=request.data['hike_session']).update(elevation_loss=checkpoint_gain + elevation_loss)

            HikingSession.objects.filter(pk=request.data['hike_session']).update(distance_traveled=Decimal(get_distance(cord1, cord2)) + Decimal(current_distance))
            return response

        if current_distance is None:
            qs = HikingCheckPoint.objects.filter(hike_session__pk=request.data['hike_session']).order_by('-created_at')[:1]
            get_location = qs.values('location')
            print('line 157', get_location)
            for current in get_location:
                current_spot = current['location']
            new_elevation = qs.values('elevation')
            print('line 161', new_elevation)
            for e in new_elevation:
                c_elevation = e['elevation']
            #print(c_elevation)

            cord2 = current_spot
            cord1 = this_location

            checkpoint_gain = calcu_elevation(c_elevation, current_elevation)
            if checkpoint_gain >= 0:
                HikingSession.objects.filter(pk=request.data['hike_session']).update(elevation_gain=checkpoint_gain)
            else:
                HikingSession.objects.filter(pk=request.data['hike_session']).update(elevation_loss=checkpoint_gain)
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