from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.exceptions import PermissionDenied


class ReservationPermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Team Managers').exists():
            raise PermissionDenied("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
        
class ManagerPermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Main Manager').exists():
            raise PermissionDenied("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

        