from django.urls import path

from . import views

urlpatterns = [
    path("profile/setup/", views.profile_setup, name="profile_setup"),
]
