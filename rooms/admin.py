from django.contrib import admin

from .models import Room, RoomStatus, Review


class RoomAdmin(admin.ModelAdmin):
    pass


class RoomStatusAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomStatus, RoomStatusAdmin)
admin.site.register(Review, ReviewAdmin)
