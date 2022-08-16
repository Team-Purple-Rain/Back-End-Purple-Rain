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
    experience_list = models.TextField(max_length=15, choices=experience_level, default=beginner, null=True, blank=True)
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
    pace_list = models.TextField(max_length=15, choices=desired_pace, default=leisure, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"


class HikingSession(TimeStamp):
    hike_user = models.ForeignKey('User', related_name='hiker', on_delete=models.CASCADE, null=True)
    distance = models.IntegerField(null=False, blank=False, default=1)
    #location is JSONField so that front-end can pass the object
    start_location = models.JSONField(null=False, blank=False)
    end_location = models.JSONField(null=True, blank=True)
    distance_traveled = models.IntegerField(null=True, blank=True)
    avg_mph = models.IntegerField(null=True, blank=True)
    #travel_time is an integerfield in secconds. Total amount to be divded by 60 to get minutes. 
    travel_time = models.IntegerField(null=True, blank=True)
    elevation_gain = models.IntegerField(null=True, blank=True)


class HikingCheckPoint(TimeStamp):
    hike_session = models.ForeignKey('HikingSession', related_name='checkpoints', on_delete=models.CASCADE)
    location = models.JSONField(null=False, blank=False)
    elevation = models.IntegerField(null=True, blank=True)
