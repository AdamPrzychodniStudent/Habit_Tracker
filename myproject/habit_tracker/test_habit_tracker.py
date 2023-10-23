from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from habit_tracker.models import Habit, CheckOff  # Adjust the import based on your project structure

@pytest.mark.django_db
def test_create_habit():
    user = User.objects.create_user(username='john', password='1234')
    
    habit = Habit.objects.create(
        user=user,
        name='Exercise',
        period=Habit.DAILY,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timezone.timedelta(days=30),
        completed=False
    )

    assert Habit.objects.count() == 1
    assert habit.name == 'Exercise'
    assert habit.period == Habit.DAILY

@pytest.mark.django_db
def test_create_checkoff():
    user = User.objects.create_user(username='john', password='1234')
    
    habit = Habit.objects.create(
        user=user,
        name='Exercise',
        period=Habit.DAILY,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timezone.timedelta(days=30),
        completed=False
    )

    checkoff = CheckOff.objects.create(habit=habit)
    
    assert CheckOff.objects.count() == 1
    assert checkoff.habit == habit
