from thatguide.models import HikingSession
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

