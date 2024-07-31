from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView

from dj.common.constants import PLAYER
from dj.matches.models import Match
from dj.matches.services import get_hero_data, get_hero_data_for_player


class MatchListView(ListView):
    model = Match
    paginate_by = 25

    def get_queryset(self):
        return Match.active_objects()


match_list_view = MatchListView.as_view()


class MatchDetailView(DetailView):
    model = Match
    slug_field = "id"
    slug_url_kwarg = "id"


match_detail_view = MatchDetailView.as_view()


@csrf_protect
@require_GET
def get_heroes_in_matches(request):
    try:
        type_obj = request.GET.get('type_obj')
        id_obj = request.GET.get('id_obj')
        league_id = request.GET.get('league_id')
        team_id = request.GET.get('team_id')
        start_date_time = request.GET.get('start_date_time')
        duration_seconds = request.GET.get('duration_seconds')

        if not type_obj or not id_obj:
            return JsonResponse({'error': 'Missing type_obj or id_obj parameter'}, status=400)

        filters = Q(game_version_id=175)
        if league_id:
            filters &= Q(league__id=league_id)
        if team_id:
            filters &= (Q(radiant_team__id=team_id) | Q(dire_team__id=team_id))
        if start_date_time:
            filters &= Q(start_date_time__gte=start_date_time)
        if duration_seconds:
            filters &= Q(duration_seconds__gte=duration_seconds)
        if type_obj == PLAYER:
            data = get_hero_data_for_player(id_obj, filters)
        else:
            data = get_hero_data(id_obj, type_obj, filters)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
