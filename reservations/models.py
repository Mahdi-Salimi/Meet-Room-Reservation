from django.db import models
from accounts.models import Team
from rooms.models import Room
from django.core.exceptions import ObjectDoesNotExist



class Reservation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return 'room:' + self.room.name + '      team:' + self.team.name 
    
    
    @staticmethod
    def retrieve_reservation(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id) 
        except ObjectDoesNotExist:
            return None
        return reservation
    
    @staticmethod
    def retrieve_reservations_list():
        reservations = Reservation.objects.all()
        return reservations
    
    @staticmethod
    def create_reservation(team, room, start_time, end_time):
        reservation = Reservation.objects.create(team=team, room=room, start_time=start_time, end_time=end_time)
        return reservation
    
    @staticmethod
    def update_reservation(reservation_id, name=None, capacity=None, is_active=None):
        try:
            reservation = Reservation.objects.get(id=reservation_id) 
        except ObjectDoesNotExist:
            return None

        if name is not None:
            reservation.name = name
        if capacity is not None:
            reservation.capacity = capacity
        if is_active is not None:
            reservation.is_active = is_active
        reservation.save()
        return reservation
    
    @staticmethod
    def delete_reservation(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id) 
            reservation.delete()
        except ObjectDoesNotExist:
            return None
        

        
