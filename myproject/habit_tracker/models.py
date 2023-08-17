from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'

    PERIOD_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    period = models.CharField(max_length=7, choices=PERIOD_CHOICES, default=DAILY)
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CheckOff(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

