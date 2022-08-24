from thatguide.models import HikingSession, User, HikingCheckPoint
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username',)

class HikeSerializer(serializers.ModelSerializer):
    hike_user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = HikingSession
        fields = ('created_at', 'updated_at', 'hike_user', 'distance', 'start_location', 'end_location', 'distance_traveled', 'avg_mph', 'travel_time', 'elevation_gain', 'current_elevation')

    def validate_start_location(self, value):
        if 'latitude' not in value or round(value['latitude']) not in range(-90, 91):
            raise serializers.ValidationError("Valid Latitude Required, Needs To Be Between -90 And 90")
        if 'longitude' not in value or round(value['longitude']) not in range(-180, 181):
            raise serializers.ValidationError("Valid Longitude Required, Needs To Be Between -180 And 180")
        return value

    def validate_distance(self, value):
        if round(value) not in range(0, 11):
            raise serializers.ValidationError("Valid Distance Required, Needs To Be Between 0.1 And 10")
        return value





class HikingCheckPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = HikingCheckPoint
        fields = '__all__'

    def validate_location(self, value):
        if 'latitude' not in value or round(value['latitude']) not in range(-90, 91):
            raise serializers.ValidationError("Valid Latitude Required, Needs To Be Between -90 And 90")
        if 'longitude' not in value or round(value['longitude']) not in range(-180, 181):
            raise serializers.ValidationError("Valid Longitude Required, Needs To Be Between -180 And 180")
        return value


class BulkCheckPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = HikingCheckPoint
        fields = '__all__'



