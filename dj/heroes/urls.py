from django.urls import path

from . import views

app_name = "heroes"

urlpatterns = [
    path("", views.heroes_list_view, name="heroes_list"),
]
