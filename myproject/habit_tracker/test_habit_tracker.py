from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from habit_tracker.models import Habit, CheckOff  

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command

from datetime import datetime, date  

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from habit_tracker.models import Habit, CheckOff
from habit_tracker.utils import update_timestamp, create_example_habits


# Test for models.py

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

# Tests for signals.py 

class SignalTests(TestCase):

    def test_create_initial_users(self):
        # Delete all existing users to simulate a fresh database
        User.objects.all().delete()

        # Ensure there are no users before running migrations
        self.assertEqual(User.objects.count(), 0)
        
        # Run migrations, which should trigger the post_migrate signal
        call_command('migrate')
        
        # Test that the users have been created
        self.assertEqual(User.objects.count(), 2)
        
        # Test that a superuser has been created
        self.assertTrue(User.objects.filter(is_superuser=True).exists())
        
        # Test that a regular user has been created
        self.assertTrue(User.objects.filter(username='user').exists())



# Tests for utils.py 

@pytest.mark.django_db
def test_create_example_habits():
    user = User.objects.create_user(username='john', password='1234')

    # There should be no habits initially
    assert Habit.objects.count() == 0

    create_example_habits(user)

    # Debug: Print all habit names to the console
    for habit in Habit.objects.all():
        print(habit.name)

    # Now there should be 7 habits created for the user
    assert Habit.objects.count() == 7


@pytest.mark.django_db
def test_create_example_habits():
    user = User.objects.create_user(username='john', password='1234')

    # There should be no habits initially
    assert Habit.objects.count() == 0

    create_example_habits(user)

    # Now there should be 6 habits created for the user
    assert Habit.objects.count() == 6

    # Check if the habits have the right number of check-offs
    exercise_habit = Habit.objects.get(name="Exercise (Time Ended)")
    assert CheckOff.objects.filter(habit=exercise_habit).count() == 7

    habit2 = Habit.objects.get(name="Read Every Day (Fully Completed)")
    assert CheckOff.objects.filter(habit=habit2).count() == 30

    habit_long_streak = Habit.objects.get(name="Meditate (Long Streak)")
    assert CheckOff.objects.filter(habit=habit_long_streak).count() == 365

    habit_short_streak = Habit.objects.get(name="Learn Something New (Short Streak)")
    assert CheckOff.objects.filter(habit=habit_short_streak).count() == 4

    kebab_habit = Habit.objects.get(name="Eat Kebab :) (Weekly)")
    assert CheckOff.objects.filter(habit=kebab_habit).count() == 3

    connect_habit = Habit.objects.get(name="Connect with Loved Ones (Monthly)")
    assert CheckOff.objects.filter(habit=connect_habit).count() == 3

# Test for forms.py 

from django.test import TestCase
from habit_tracker.forms import HabitForm

# Test for forms.py

class HabitFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'name': 'Test Habit',
            'period': 'Daily',
            'start_date': '2022-01-01',
            'end_date': '2022-12-31'
        }
        form = HabitForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'name': '',  # name is empty
            'period': 'Daily',
            'start_date': '2022-01-01',
            'end_date': '2022-12-31'
        }
        form = HabitForm(data)
        self.assertFalse(form.is_valid())
        
    def test_required_fields(self):
        data = {
            # Missing 'name' and 'period'
            'start_date': '2022-01-01',
            'end_date': '2022-12-31'
        }
        form = HabitForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors.keys()), {'name', 'period'})

    def test_date_constraints(self):
        data = {
            'name': 'Test Habit',
            'period': 'Daily',
            'start_date': '2022-12-31',  # start_date > end_date
            'end_date': '2022-01-01'
        }
        form = HabitForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('end_date', form.errors)
