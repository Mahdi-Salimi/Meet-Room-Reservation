from django import forms
from django.contrib.auth import get_user_model

from .models import Room, RoomStatus, Review


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RoomStatusForm(forms.ModelForm):
    class Meta:
        model = RoomStatus
        fields = ['room', 'start_time', 'end_time']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if hasattr(self, 'is_empty'):
            instance.is_empty = self.is_empty
        if commit:
            instance.save()
        return instance


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['room', 'content', 'rating']



    def save(self, commit=True):
        instance = super().save(commit=False)
        if hasattr(self, 'user_id'):
            instance.user_id = self.user_id
        if commit:
            instance.save()
        return instance
