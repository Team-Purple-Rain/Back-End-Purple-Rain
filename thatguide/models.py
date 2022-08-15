from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class HikingSession(TimeStamp):
    #hike_user = models.ForeignKey('User', related_name='hiker', on_delete=models.CASCADE)
    one = 1
    five = 5
    ten = 10
    distance_choice = [
        (one, '1 mile'),
        (five, '5 miles'),
        (ten, '10 miles'),
    ]
    distance_list = models.IntegerField(choices=distance_choice, default=one)
    #location is JSONField so that front-end can pass the object
    start_location = models.JSONField(null=False, blank=False)
    end_location = models.JSONField(null=True, blank=True)
    distance_traveled = models.IntegerField(null=True, blank=True)
    avg_mph = models.IntegerField(null=True, blank=True)
    #travel_time is an integerfield in secconds. Total amount to be divded by 60 to get minutes. 
    travel_time = models.IntegerField(null=True, blank=True)
    elevation_gain = models.IntegerField(null=True, blank=True)
    
