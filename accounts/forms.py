from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Profile, Team, OTPCode


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email']

        widgets = {
            'email': forms.EmailInput()
        }


class OTPValidationForm(forms.ModelForm):
    class Meta:
        model = OTPCode
        fields = ['email', 'code']

        widgets = {
            'email': forms.EmailInput(),
            'code': forms.TextInput()
        }


class ProfileDetailForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'username', 'first_name', 'last_name', 'image']

        widgets = {
            'email': forms.EmailInput(),
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'image': forms.FileInput(attrs={'accept': 'image/*'})

        }


class TeamCreateForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(team__isnull=True), required=False)
    manager = forms.ModelChoiceField(queryset=get_user_model().objects.filter(team__isnull=True), required=True)

    class Meta:
        model = Team
        fields = ['name', 'manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = get_user_model().objects.filter(team__isnull=True)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m() 
        return instance