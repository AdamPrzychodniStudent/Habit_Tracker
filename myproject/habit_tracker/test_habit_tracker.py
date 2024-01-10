from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from habit_tracker.models import Habit, CheckOff  

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command

from datetime import datetime, date, timedelta  

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from habit_tracker.models import Habit, CheckOff
from habit_tracker.utils import update_timestamp, create_example_habits

from django.test import TestCase
from habit_tracker.forms import HabitForm

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()



# Tests for models.py

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


# Setup 

class HabitTestBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.habit = Habit.objects.create(
            user=self.user,
            name="Test Habit",
            period="Daily",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            completed=False
        )


# Test for forms.py 

class HabitFormTest(HabitTestBase):  

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


# Tests for views.py

from django.test import TestCase
from django.urls import reverse

class WelcomeViewTest(TestCase):
    def test_welcome_view(self):

        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/welcome.html')


class HabitListViewTest(HabitTestBase):  
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_habit_list(self):
        response = self.client.get(reverse('habit_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/habit_list.html')


class CreateHabitViewTest(HabitTestBase):  
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_habit_get(self):
        response = self.client.get(reverse('create_habit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/create_habit.html')

    def test_create_habit_post(self):
        response = self.client.post(reverse('create_habit'), {
            'name': 'Exercise',
            'period': 'Daily',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        })
        self.assertRedirects(response, reverse('habit_list'))
        self.assertEqual(Habit.objects.count(), 1)


class EditHabitViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.habit = Habit.objects.create(
            user=self.user, 
            name="Test Habit", 
            period="Daily", 
            start_date=date.today(), 
            end_date=date.today() + timedelta(days=30),
            completed=False
        )
        
    def test_edit_habit_get(self):
        response = self.client.get(reverse('edit_habit', args=[self.habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/edit_habit.html')
        
    def test_edit_habit_post_checkoff(self):
        response = self.client.post(reverse('edit_habit', args=[self.habit.id]), {'check_off': 'true'})
        self.habit.refresh_from_db()
        self.assertTrue(self.habit.completed)
        
    def test_edit_habit_post_delete(self):
        response = self.client.post(reverse('edit_habit', args=[self.habit.id]), {'delete_habit': 'true'})
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())


class EditHabitViewTest(HabitTestBase):  
    
    def test_edit_habit_get(self):
        response = self.client.get(reverse('edit_habit', args=[self.habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/edit_habit.html')
        
    def test_edit_habit_post_checkoff(self):
        response = self.client.post(reverse('edit_habit', args=[self.habit.id]), {'check_off': 'true'})
        self.habit.refresh_from_db()
        self.assertTrue(self.habit.completed)
        
    def test_edit_habit_post_delete(self):
        response = self.client.post(reverse('edit_habit', args=[self.habit.id]), {'delete_habit': 'true'})
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())


class ToggleHabitDoneTest(HabitTestBase):  

    def test_toggle_habit_done(self):
        initial_count = CheckOff.objects.filter(habit=self.habit).count()
        self.client.get(reverse('toggle_habit_done', args=[self.habit.id]))
        final_count = CheckOff.objects.filter(habit=self.habit).count()
        self.assertEqual(final_count, initial_count + 1)
        

class ShowCurrentHabitsTest(HabitTestBase):  
    
    def test_show_current_habits(self):
        response = self.client.get(reverse('show_current_habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/current_habits.html')
        self.assertIn(self.habit, response.context['current_habits'])




class HabitViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.habit = Habit.objects.create(
            user=self.user,
            name="Test Habit",
            period="Daily",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            completed=False
        )

    def test_show_same_periodicity_habits(self):
        response = self.client.get(reverse('show_same_periodicity_habits', args=['Daily']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/same_periodicity_habits.html')
        self.assertIn(self.habit, response.context['habits'])

    def test_show_completed_habits(self):
        response = self.client.get(reverse('show_completed_habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/completed_habits.html')

    def test_show_streaks(self):
        response = self.client.get(reverse('show_streaks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/show_streaks.html')


class HabitStruggleRepetitionTestBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.habit_daily = Habit.objects.create(
            user=self.user,
            name="Test Habit Daily",
            period=Habit.DAILY,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            completed=False
        )
        self.habit_weekly = Habit.objects.create(
            user=self.user,
            name="Test Habit Weekly",
            period=Habit.WEEKLY,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            completed=False
        )


class ShowStruggledHabitsTest(HabitStruggleRepetitionTestBase):
    def test_show_struggled_habits(self):
        # Create some CheckOffs to simulate habits being followed or missed
        CheckOff.objects.create(habit=self.habit_daily)
        
        response = self.client.get(reverse('show_struggled_habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/show_struggled_habits.html')
        
        struggled_habits = response.context['struggled_habits']
        self.assertEqual(len(struggled_habits), 2)  # You should have 2 habits in the test setup
        
        for habit_data in struggled_habits:
            if habit_data['name'] == 'Test Habit Daily':
                self.assertLess(habit_data['struggle_score'], 50)  # Assuming you're struggling less with this habit
            else:
                self.assertGreaterEqual(habit_data['struggle_score'], 50)  # Assuming you're struggling more with this habit


class ShowRepetitionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a daily habit with 30 repetitions
        self.habit_daily = Habit.objects.create(
            user=self.user,
            name='Test Habit Daily',
            period=Habit.DAILY,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=29),
            completed=False
        )
        
        # Create a weekly habit with 4 repetitions
        self.habit_weekly = Habit.objects.create(
            user=self.user,
            name='Test Habit Weekly',
            period=Habit.WEEKLY,
            start_date=date.today(),
            end_date=date.today() + timedelta(weeks=3),
            completed=False
        )

    def test_show_repetitions(self):
        # Create some CheckOffs to simulate habits being followed
        CheckOff.objects.create(habit=self.habit_daily)
        
        response = self.client.get(reverse('show_repetitions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/show_repetitions.html')
        
        habit_repetitions = response.context['habit_repetitions']
        self.assertEqual(len(habit_repetitions), 2)  # You should have 2 habits in the test setup
        
        for habit_data in habit_repetitions:
            if habit_data['name'] == 'Test Habit Daily':
                self.assertEqual(habit_data['remaining_reps'], 29)  # 30 - 1 = 29
            elif habit_data['name'] == 'Test Habit Weekly':
                self.assertEqual(habit_data['remaining_reps'], 3)  # No CheckOffs for this habit, so remaining reps should be 3

