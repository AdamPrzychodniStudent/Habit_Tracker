from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    period = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class CheckOff(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)