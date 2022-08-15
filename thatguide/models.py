from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class HikingSession(TimeStamp):
    #hike_user = models.ForeignKey('User', related_name='hiker', on_delete=models.CASCADE)
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    distance_choice = [
        (one, '1 mile'),
        (two, '2 miles'),
        (three, '3 miles'),
        (four, '4 miles'),
        (five, '5 miles'),
        (six, '6 miles'),
        (seven, '7 miles'),
        (eight, '8 miles'),
        (nine, '9 miles'),
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
    
