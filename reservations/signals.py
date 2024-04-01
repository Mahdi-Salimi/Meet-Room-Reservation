from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from rooms.models import RoomStatus
from .models import Reservation


@receiver(post_save, sender=Reservation)
def handle_reservation(sender, instance, created, **kwargs):
    if created:
        overlapping_reservations = RoomStatus.objects.filter(
            room=instance.room.id,
            start_time__lt=instance.end_time,
            end_time__gt=instance.start_time
        )

        if overlapping_reservations.exists():
            error_message = "There's already a reservation for this room in this time."
            raise ValidationError(error_message)
        else:
            RoomStatus.objects.create(
                room=instance.room,
                team=instance.team,
                start_time=instance.start_time,
                end_time=instance.end_time,
                is_empty=False
            )
    elif kwargs.get('update_fields') is not None:
        overlapping_reservations = RoomStatus.objects.filter(
            room=instance.room,
            start_time__lt=instance.end_time,
            end_time__gt=instance.start_time
        ).exclude(pk=instance.pk)

        if overlapping_reservations.exists():
            error_message = "There's already a reservation for this room in this time."
            raise ValidationError(error_message)
        else:
            room_status = RoomStatus.objects.get(room=instance.room)
            room_status.team = instance.team
            room_status.start_time = instance.start_time
            room_status.end_time = instance.end_time
            room_status.is_empty = False  
            room_status.save()

@receiver(post_delete, sender=Reservation)
def handle_reservation_deletion(sender, instance, **kwargs):
    filter_kwargs = {field.name: getattr(instance, field.name) for field in instance._meta.fields if not field.primary_key}
    deleted_room_statuses = RoomStatus.objects.filter(**filter_kwargs)
    deleted_room_statuses.delete()


@receiver(post_save, sender=RoomStatus)
def send_reservation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'New reservation'
        message = (f'A new reservation for room {instance.room.name} '
                   f'from {instance.start_time} to {instance.end_time} has been created.')
        emails = [member.email for member in instance.team.profile_set.all()]
        from_email = DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, emails, fail_silently=False)
    else:
        if instance.is_empty:
            subject = 'Reservation canceled'
            message = (f'The reservation for room {instance.room.name} '
                       f'from {instance.start_time} to {instance.end_time} has been canceled.')
            emails = [member.email for member in instance.team.profile_set.all()]
            from_email = DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, emails, fail_silently=False)

        else:
            subject = 'Reservation updated'
            message = (f'The reservation for room {instance.room.name} '
                       f'from {instance.start_time} to {instance.end_time} has been updated.')
            emails = [member.email for member in instance.team.profile_set.all()]
            from_email = DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, emails, fail_silently=False)
