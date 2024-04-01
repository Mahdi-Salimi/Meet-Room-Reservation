from .models import Reservation
from django import forms
from django.forms import DateTimeInput


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['team', 'room', 'start_time', 'end_time']
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

