from thatguide.models import HikingSession
from rest_framework import serializers


class HikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HikingSession
        fields = '__all__'
