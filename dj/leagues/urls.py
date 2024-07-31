from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "leagues"

urlpatterns = [
    path("<int:league_id>/", views.league_detail_view, name="league_detail"),
    path("<int:league_id>/update/", login_required(views.update_league_data), name="update_league_data"),
    path("<int:series_id>/series/", login_required(views.update_series_matches), name="league_update_series"),
    path("", views.league_list_view, name="league_list"),
    path("update/", login_required(views.update_leagues_list), name="leagues_update"),
]
