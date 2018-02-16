from django.forms import ModelForm
from workouts.models import WorkoutSession

class WorkoutSessionForm(ModelForm):
    class Meta:
        model = WorkoutSession
        fields = [
            'name',
            'description',
            'location',
            'workout_date',
        ]
