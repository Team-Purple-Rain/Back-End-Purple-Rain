from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStamp(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class User(AbstractUser):
    # experience level choices
    beginner = 'beginner'
    medium = 'medium'
    advanced = 'advanced'
    experience_level = [
        ('', 'EMPTY'),
        (beginner, 'beginner'),
        (medium, 'medium'),
        (advanced, 'advanced'),
    ]
    # desired pace choices
    leisure = 'leisure'
    powerwalk = 'powerwalk'
    chased_by_bear = 'chased by bear'
    desired_pace = [
        ('', 'EMPTY'),
        (leisure, 'leisure'),
        (powerwalk, 'powerwalk'),
        (chased_by_bear, 'chased by bear'),
    ]
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"


class HikingSession(TimeStamp):
    # hike_user = models.ForeignKey('User', related_name='hiker', on_delete=models.CASCADE, null=True)
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

