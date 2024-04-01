import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, FormView, ListView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView



from .forms import ProfileCreateForm, TeamCreateForm, OTPValidationForm, ProfileDetailForm
from .models import OTPCode
from .models import Team, Profile
from reservations.permissions import ManagerPermissionMixin


User = get_user_model()

class SignupCreateOTP(FormView):
    template_name = 'accounts/profile/signup.html'
    form_class = ProfileCreateForm
    success_url = '/accounts/signup/otp'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        otp = self._generate_otp()

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            messages.error(self.request, 'This email is already exist')
            return self.form_invalid(form)

        User.objects.create(email=email, username=email)
        OTPCode.objects.create(email=email, code=otp)
        send_mail(
            'Your OTP for Login',
            f'{otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return super().form_valid(form)

    def get_success_url(self):
        email = self.request.POST.get('email')
        return reverse('accounts:signup_otp') + f'?email={email}'

    def _generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])


class SignupOTP(FormView):
    template_name = 'accounts/profile/signup_otp.html'
    form_class = OTPValidationForm
    success_url = '/rooms'

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.GET.get('email', '')
        return initial

    def form_valid(self, form):
        email = form.cleaned_data['email']
        otp = form.cleaned_data['code']

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            user_otp = OTPCode.objects.filter(email=email, code=otp).exists()
            if user_otp:
                user = existing_user
                login(self.request, user)
            else:
                existing_user.delete()
                messages.error(self.request, 'Wrong OTP or Email!')
                return self.form_invalid(form)

        return super().form_valid(form)
    
    def get_success_url(self):
        email = self.request.POST.get('email')
        existing_user = User.objects.get(email=email)
        if existing_user.is_manager:
            return reverse('accounts:manager_user')
        elif existing_user.is_team_manager:
            return reverse('accounts:team_manager_user')
        else:
            return reverse('accounts:normal_user')


class RequestOTPCreate(FormView):
    template_name = 'accounts/profile/login.html'
    form_class = ProfileCreateForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        otp = self._generate_otp()

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            existing_otp = OTPCode.objects.filter(email=email).first()
            if existing_otp:
                existing_otp.code = otp
                existing_otp.save()
            else:
                OTPCode.objects.create(email=email, code=otp)
        else:
            messages.error(self.request, 'You are not a User Please Signup first')
            return self.form_invalid(form)

        send_mail(
            'Your OTP for Login',
            f'{otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_success_url(self):
        email = self.request.POST.get('email')
        return reverse('accounts:login_otp') + f'?email={email}'

    def _generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])


class LoginOTP(FormView):
    template_name = 'accounts/profile/login_otp.html'
    form_class = OTPValidationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.GET.get('email', '')
        return initial

    def form_valid(self, form):
        email = form.cleaned_data['email']
        otp = form.cleaned_data['code']

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            user_otp = OTPCode.objects.filter(email=email, code=otp).exists()
            if user_otp:
                user = existing_user
                login(self.request, user)
            else:
                messages.error(self.request, 'Wrong OTP!')
                return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        email = self.request.POST.get('email')
        existing_user = User.objects.get(email=email)
        if existing_user.is_manager:
            return reverse('accounts:manager_user')
        elif existing_user.is_team_manager:
            return reverse('accounts:team_manager_user')
        else:
            return reverse('accounts:normal_user')        

class CustomLogoutView(LogoutView):
    template_name = 'accounts/profile/logout.html'  
    next_page = reverse_lazy('home')
    
    

def normal_user_view(request):
    return render(request, 'accounts/profile/normal_user.html')


def manager_user_view(request):
    return render(request, 'accounts/profile/manager_user.html')


def team_manager_user_view(request):
    return render(request, 'accounts/profile/team_manager_user.html')


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileDetailForm
    template_name = 'accounts/profile/profile_detail.html'
    success_url = '/accounts/normal_user'

    def get_object(self, queryset=None):
        return self.request.user


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamCreateForm
    template_name = 'accounts/Team/team_create.html'
    success_url = '/accounts/teams/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        team = form.instance
        name = team.name
        users = form.cleaned_data.get('users', [])
        for user in users:
            user.team = Team.objects.get(name=name)
            user.save()
        manager = form.cleaned_data['manager']
        manager.is_team_manager = True
        manager.team = team
        manager.save()
        return response


class TeamDetailView(ManagerPermissionMixin ,DetailView):
    model = Team
    template_name = 'accounts/Team/team_detail.html'


class TeamListView(ManagerPermissionMixin ,ListView):
    model = Team
    template_name = 'accounts/Team/team_list.html'
    context_object_name = 'teams'


class TeamUpdateView(ManagerPermissionMixin ,UpdateView):
    model = Team
    form_class = TeamCreateForm
    template_name = 'accounts/Team/team_update.html'
    success_url = '/accounts/teams/'


class TeamDeleteView(ManagerPermissionMixin ,DeleteView):
    model = Team
    template_name = 'accounts/Team/team_delete.html'
    success_url = '/accounts/teams/'
