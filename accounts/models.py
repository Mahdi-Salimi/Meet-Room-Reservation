from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    phone_number = models.CharField(null=True, blank=True, max_length=11)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, default=None, null=True, blank=True)
    is_manager = models.BooleanField(default=False, null=True, blank=True)
    is_team_manager = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    @staticmethod
    def create_profile(username, password, first_name, last_name, email, image):
        userprofile = Profile(username=username,
                              first_name=first_name,
                              last_name=last_name,
                              email=email,
                              image=image
                              )
        userprofile.set_password(raw_password=password)
        userprofile.save()
        return userprofile

    @staticmethod
    def retrieve_profile(user_id):
        userprofile = Profile.objects.get(id=user_id)

        return userprofile

    @staticmethod
    def delete_profile(user_id):
        userprofile = Profile.objects.get(id=user_id)
        userprofile.delete()

        return userprofile

    @staticmethod
    def update_profile(user_id, first_name=None, last_name=None, email=None, password=None, image=None):
        userprofile = Profile.objects.get(id=user_id)
        if first_name is not None:
            userprofile.first_name = first_name
        if last_name is not None:
            userprofile.last_name = last_name
        if email is not None:
            userprofile.email = email
        if password is not None:
            userprofile.password = password
        if image is not None:
            userprofile.image = image
        userprofile.save()

        return userprofile


class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='manager_team')
    
    def __str__(self):
        return self.name

    @staticmethod
    def create_team(name, member, manager):
        team = Team.objects.create(name=name, member=member, manager=manager)
        return team

    @staticmethod
    def retrieve_team(team_id):
        return Team.objects.get(id=team_id)

    @staticmethod
    def update_team(team_id, name=None, member=None, manager=None):
        team = Team.retrieve_team(team_id)
        if name is not None:
            team.name = name
        if member is not None:
            team.member = member
        if manager is not None:
            team.manager = manager
        team.save()
        return team

    @staticmethod
    def delete_team(team_id):
        team = Team.retrieve_team(team_id)
        team.delete()
        return team


class OTPCode(models.Model):
    code = models.CharField(max_length=6)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
