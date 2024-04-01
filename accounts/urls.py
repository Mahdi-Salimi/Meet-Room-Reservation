from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('teams/', views.TeamListView.as_view(), name='team'),
    path('teams/create/', views.TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('teams/<int:pk>/update/', views.TeamUpdateView.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),
    path('login/', views.RequestOTPCreate.as_view(), name='login'),
    path('login/otp/', views.LoginOTP.as_view(), name='login_otp'),
    path('signup/', views.SignupCreateOTP.as_view(), name='signup'),
    path('signup/otp/', views.SignupOTP.as_view(), name='signup_otp'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),   
    path('normal_user/', views.normal_user_view, name='normal_user'),
    path('manager_user/', views.manager_user_view, name='manager_user'),
    path('team_manager_user/', views.team_manager_user_view, name='team_manager_user'),
    path('profile_detail/', views.ProfileEditView.as_view(), name='profile_detail'),

]