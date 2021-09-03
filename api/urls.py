from django.urls import path
# import api class and functional view
from api import views

app_name = 'api'
urlpatterns = [
    path('registration/', views.Register_Users, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
