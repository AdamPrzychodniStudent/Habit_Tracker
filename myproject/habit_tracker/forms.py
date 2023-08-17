from django import forms
from .models import Habit

class DateInput(forms.DateInput):
    input_type = 'date'

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'period', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

