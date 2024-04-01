from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Profile, OTPCode, Team


class ProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'team', 'is_staff', 'is_active', 'is_manager', 'is_team_manager')
    list_filter = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'team', 'is_manager', 'is_team_manager', 'image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','user_permissions', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email', 'username', 'first_name', 'last_name')


class TeamAdmin(admin.ModelAdmin):
    pass


class OTPCodeAdmin(admin.ModelAdmin):
    pass

    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team)
admin.site.register(OTPCode, OTPCodeAdmin)
