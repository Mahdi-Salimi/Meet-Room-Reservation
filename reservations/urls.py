from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='reservations'),
    path('reservation_all', views.ReservationAllListView.as_view(), name='reservations_all'),
    path('create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),

]