from thatguide.models import HikingSession, User, HikingCheckPoint
from rest_framework import serializers


class HikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HikingSession
        fields = '__all__'

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


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
