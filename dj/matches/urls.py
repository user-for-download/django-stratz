from django.urls import path

from dj.matches.views import match_list_view, match_detail_view, get_heroes_in_matches

app_name = "matches"

urlpatterns = [
    path("<int:id>/", view=match_detail_view, name="match_detail"),
    path("", view=match_list_view, name="match_list"),
    path("heroes", view=get_heroes_in_matches, name="matches_heroes"),
]
