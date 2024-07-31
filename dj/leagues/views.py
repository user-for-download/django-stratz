from celery import current_app
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView, DetailView
from orjson import orjson

from dj.leagues.models import League, Series


class LeagueListView(ListView):
    model = League
    paginate_by = 25

    def get_queryset(self):
        return League.objects.tier2()


league_list_view = LeagueListView.as_view()


class LeagueDetailView(DetailView):
    model = League
    slug_field = "id"
    slug_url_kwarg = "league_id"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = self.object

        # Get series and paginate
        series = league.series.active().select_related(
            'team_one', 'team_two'
        )

        page_obj = self.paginate_series(series)
        teams = self.get_teams(series)
        # graph_data = get_hero_data(league.id, 'league')

        context.update({
            'teams': teams,
            'page_obj': page_obj,
        })
        return context

    def paginate_series(self, series):
        paginator = Paginator(series, self.paginate_by)
        page_number = self.request.GET.get('page')
        return paginator.get_page(page_number)

    @staticmethod
    def get_teams(series):
        team_ids = set()
        for series_obj in series:
            team_ids.add(series_obj.team_one)
            team_ids.add(series_obj.team_two)
        return list(team_ids)


# Usage
league_detail_view = LeagueDetailView.as_view()


@csrf_protect
@require_POST
def update_leagues_list(request):
    try:
        current_app.send_task(name="dj.leagues.tasks.task_get_and_save_leagues_list")
        messages.success(request, 'Task "Update Leagues" is running!')
    except Exception as e:
        messages.error(
            request,
            f'Exception occurred while running the task "Update Leagues": {str(e)}',
        )

    return redirect("/leagues/")


@csrf_protect
@require_POST
def update_league_data(request, league_id):
    if not league_id:
        messages.error(request, "League ID is required.")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    try:
        league, _ = League.objects.get_or_create(id=league_id)
        current_app.send_task(
            "dj.leagues.tasks.task_get_and_save_league_series", args=[league.id, True]
        )
        messages.success(request, 'Task "Update League Data" is running!')
    except League.DoesNotExist:
        messages.error(request, "League not found.")
    except Exception as e:
        messages.error(request, f"Exception occurred: {str(e)}")

    return redirect(f"/leagues/{league_id}/")


@csrf_protect
@require_GET
def update_series_matches(request, series_id):
    try:
        series, _ = Series.objects.get_or_create(id=series_id)
        series_data = {
            'id': series.id,
            'win': series.winning_team_id,
        }
        current_app.send_task(
            "dj.matches.tasks.task_get_and_save_object_matches", args=['series', series_id]
        )
        response_data = orjson.dumps(series_data)
        return HttpResponse(response_data, content_type='application/json')
    except Series.DoesNotExist:
        response_data = orjson.dumps({'error': 'Series not found'})
        return HttpResponse(response_data, content_type='application/json', status=404)
