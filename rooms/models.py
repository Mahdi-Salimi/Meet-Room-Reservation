from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Team


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def retrieve_room(room_id):
        try:
            room = Room.objects.get(id=room_id)
        except ObjectDoesNotExist:
            return None
        return room

    @staticmethod
    def retrieve_rooms_list():
        rooms = Room.objects.all()
        return rooms

    @staticmethod
    def create_room(name, capacity, is_active=True):
        room = Room.objects.create(name=name, capacity=capacity, is_active=is_active)
        return room

    @staticmethod
    def update_room(room_id, name=None, capacity=None, is_active=None):
        try:
            room = Room.objects.get(id=room_id)
        except ObjectDoesNotExist:
            return None

        if name is not None:
            room.name = name
        if capacity is not None:
            room.capacity = capacity
        if is_active is not None:
            room.is_active = is_active
        room.save()
        return room

    @staticmethod
    def delete_room(room_id):
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
        except ObjectDoesNotExist:
            return None


class RoomStatus(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_empty = models.BooleanField(default=True)

    def __str__(self):
        return (f"{self.room.name} from {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"to {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    @staticmethod
    def retrieve_room_status(room_status_id):
        try:
            room_status = RoomStatus.objects.get(id=room_status_id)
        except ObjectDoesNotExist:
            return None
        return room_status

    @staticmethod
    def retrieve_room_statuses_list():
        room_statuses = RoomStatus.objects.all()
        return room_statuses

    @staticmethod
    def create_room_status(room, start_time, end_time, is_empty=True):
        room_status = RoomStatus.objects.create(room=room, start_time=start_time, end_time=end_time, is_empty=is_empty)
        return room_status

    @staticmethod
    def update_room_status(room_status_id, room=None, start_time=None, end_time=None, is_empty=None):
        try:
            room_status = RoomStatus.objects.get(id=room_status_id)
        except ObjectDoesNotExist:
            return None

        if room is not None:
            room_status.room = room
        if start_time is not None:
            room_status.start_time = start_time
        if end_time is not None:
            room_status.end_time = end_time
        if is_empty is not None:
            room_status.is_empty = is_empty
        room_status.save()
        return room_status

    @staticmethod
    def delete_room_status(room_status_id):
        try:
            room_status = RoomStatus.objects.get(id=room_status_id)
            room_status.delete()
        except ObjectDoesNotExist:
            return None


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room.name
    
    @staticmethod
    def retrieve_review(review_id):
        try:
            review = Review.objects.get(id=review_id) 
        except ObjectDoesNotExist:
            return None
        return review
    
    @staticmethod
    def retrieve_reviews_list():
        reviews = Review.objects.all()
        return reviews
    
    @staticmethod
    def create_review(room, user, content, rating):
        review = Review.objects.create(room=room, user=user, content=content, rating=rating)
        return review
    
    @staticmethod
    def update_review(review_id, content=None, rating=None):
        try:
            review = Review.objects.get(id=review_id) 
        except ObjectDoesNotExist:
            return None

        if content is not None:
            review.content = content
        if rating is not None:
            review.rating = rating

        review.save()
        return review
    
    @staticmethod
    def delete_review(review_id):
        try:
            review = Review.objects.get(id=review_id) 
            review.delete()
        except ObjectDoesNotExist:
            return None
