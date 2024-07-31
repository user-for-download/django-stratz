from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "players"

urlpatterns = [
    path("<int:player_id>/", views.player_detail_view, name="player_detail"),
    path("update/<int:player_id>/", login_required(views.update_player_data), name="player_update"),
    path("", views.player_list_view, name="player_list"),
    path("update/", login_required(views.get_players), name="players_update"),
]
