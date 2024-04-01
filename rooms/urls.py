from django.urls import path

from . import views

app_name = 'rooms'
urlpatterns = [
    path('', views.RoomListView.as_view(), name='rooms'),
    path('rooms_all/', views.RoomAllListView.as_view(), name='rooms_all'),
    path('create/', views.RoomCreateView.as_view(), name='room_create'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('<int:pk>/update/', views.RoomUpdateView.as_view(), name='room_update'),
    path('<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),

    path('roomstatus/', views.RoomStatusListView.as_view(), name='room_statuses'),
    path('roomstatus/create/', views.RoomStatusCreateView.as_view(), name='room_status_create'),
    path('roomstatus/<int:pk>/', views.RoomStatusDetailView.as_view(), name='room_status_detail'),
    path('roomstatus/<int:pk>/update/', views.RoomStatusUpdateView.as_view(), name='room_status_update'),
    path('roomstatus/<int:pk>/delete/', views.RoomStatusDeleteView.as_view(), name='room_status_delete'),
    
    path('review/', views.ReviewListView.as_view(), name='reviews'),
    path('review/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]
