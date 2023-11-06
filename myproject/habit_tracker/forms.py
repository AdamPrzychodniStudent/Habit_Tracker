from django import forms
from django.core.exceptions import ValidationError
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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                self.add_error('end_date', 'End date should be after start date.')
                raise ValidationError('End date should be after start date.')
