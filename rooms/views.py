from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, ReviewForm
from .models import Room, RoomStatus, Review
from reservations.permissions import ManagerPermissionMixin


# Room views
class RoomCreateView(LoginRequiredMixin,ManagerPermissionMixin,CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_create.html'
    success_url = '/rooms/'


class RoomDetailView(LoginRequiredMixin,DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'

class RoomAllListView(ListView):
    model = Room
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'
    
    def get_queryset(self):
        queryset = Room.objects.all()
        return queryset
    
class RoomListView(ListView):
    model = Room
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'
    
    def get_queryset(self):
        queryset = Room.objects.filter(is_active = True)
        return queryset


class RoomUpdateView(LoginRequiredMixin,ManagerPermissionMixin,UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_create.html'
    success_url = '/rooms/'


class RoomDeleteView(LoginRequiredMixin,ManagerPermissionMixin,DeleteView):
    model = Room
    template_name = 'rooms/room_delete.html'
    success_url = '/rooms/'


# RoomStatus views
class RoomStatusCreateView(LoginRequiredMixin,CreateView):
    model = RoomStatus
    fields = '__all__'
    template_name = 'rooms/room_create.html'
    success_url = '/rooms/'


class RoomStatusDetailView(LoginRequiredMixin,DetailView):
    model = RoomStatus
    template_name = 'rooms/room_status_detail.html'


class RoomStatusListView(LoginRequiredMixin,ListView):
    model = RoomStatus
    template_name = 'rooms/room_status_list.html'
    context_object_name = 'room_statuses'
    
    def get_queryset(self):
        queryset = RoomStatus.objects.filter(team = self.request.user.team)
        return queryset


class RoomStatusUpdateView(LoginRequiredMixin,UpdateView):
    model = RoomStatus
    fields = '__all__'
    template_name = 'rooms/room_create.html'
    success_url = '/rooms/'


class RoomStatusDeleteView(LoginRequiredMixin,DeleteView):
    model = RoomStatus
    template_name = 'rooms/room_delete.html'
    success_url = '/rooms/'


# Review Views

class ReviewCreateView(LoginRequiredMixin,CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'rooms/review_create.html'
    success_url = '/accounts/normal_user'
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin,DetailView):
    model = Review
    template_name = 'rooms/review_detail.html'


class ReviewListView(LoginRequiredMixin,ListView):
    model = Review
    template_name = 'rooms/review.html'
    context_object_name = 'reviews'


class ReviewUpdateView(LoginRequiredMixin,UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'rooms/review_update.html'
    success_url = '/rooms/'


class ReviewDeleteView(LoginRequiredMixin,DeleteView):
    model = Review
    template_name = 'rooms/review_delete.html'
    success_url = '/rooms/'
