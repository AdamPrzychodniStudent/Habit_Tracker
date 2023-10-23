from django import forms
from .models import Habit

# Custom DateInput widget for date fields
class DateInput(forms.DateInput):
    input_type = 'date'

# Create a ModelForm for the Habit model
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        # Fields to include in the form
        fields = ['name', 'period', 'start_date', 'end_date']
        # Widgets to use for specific fields
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
