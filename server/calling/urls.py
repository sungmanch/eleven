from django.urls import path

from . import views

app_name = "calling"

urlpatterns = [
    path("talk/", views.talk_to_eleven, name="talk"),
]
