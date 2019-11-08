from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(User):
    image = models.ImageField()


class Course(models.Model):
    department = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    course_number = models.IntegerField()
    group_number = models.IntegerField()
    teacher = models.CharField(max_length=60)
    start_time = models.TimeField()
    end_time = models.TimeField()
    first_day = models.CharField(max_length=30)
    second_day = models.CharField(max_length=30)