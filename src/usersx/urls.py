from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('token', views.get_token),
    path('auth', views.auth),
    path('users', views.list_users),
    path('<str:loggedin_user>/<str:user>/follow', views.follow),
    path('<str:username>/followers', views.get_followers),
    path('<str:username>/following', views.get_following),
]
