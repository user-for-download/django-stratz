# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "teams"

urlpatterns = [
    path("<int:id>/", views.team_detail_view, name="team_detail"),
    path("update/<int:team_id>/", login_required(views.update_team_data), name="update_item"),
    path("", views.team_list_view, name="team_list"),
    path("update/", views.get_teams, name="teams_update"),
]
