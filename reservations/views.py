from django.shortcuts import render
from .forms import ReservationForm
from .models import Reservation
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from .permissions import ReservationPermissionMixin, ManagerPermissionMixin
from django.http import HttpResponseRedirect
from rooms.models import RoomStatus


# Reservation Views
class ReservationCreateView(ReservationPermissionMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_create.html'
    success_url = '/accounts/team_manager_user/'
    
    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room_id')
        if room_id:
            initial['room'] = room_id
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_statuses = RoomStatus.objects.all()
        context['room_statuses'] = room_statuses
        return context
    



class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'


class ReservationAllListView(ManagerPermissionMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservations_list.html'
    context_object_name = 'reservations'
    
    def get_queryset(self):
        user_team = self.request.user.team

        queryset = super().get_queryset().all()
        
        return queryset
    

class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservations/reservations_list.html'
    context_object_name = 'reservations'
    
    def get_queryset(self):
        user_team = self.request.user.team

        queryset = super().get_queryset().filter(team=user_team)
        
        return queryset


class ReservationUpdateView(ReservationPermissionMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_create.html'
    success_url = '/reservations'


class ReservationDeleteView(ReservationPermissionMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_delete.html'
    success_url = '/reservations'