from celery import current_app
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic import ListView

from dj.leagues.models import League
from dj.matches.models import Match
from dj.teams.models import Team


class TeamListView(ListView):
    model = Team
    paginate_by = 25

    def get_queryset(self):
        # Calculate win_ratio with proper handling of null and zero values
        return Team.objects.is_pro()
    #
    # .annotate(
    #     win_ratio=ExpressionWrapper(
    #         Case(
    #             When(win_count__isnull=True, then=Value(0)),
    #             When(loss_count__isnull=True, then=Value(0)),
    #             When(win_count=0, then=Value(0)),
    #             When(loss_count=0, then=Value(0)),
    #             default=F('win_count') * 100.0 / (F('win_count') + F('loss_count')),
    #             output_field=FloatField()
    #         ),
    #         output_field=FloatField()
    #     )
    # ).order_by('-win_ratio')


team_list_view = TeamListView.as_view()


class TeamDetailView(DetailView):
    """
    View for displaying detailed information about a team.
    """
    model = Team
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object

        # matches = self.get_team_matches(team)
        leagues = self.get_team_leagues(team)

        context.update({
            # 'matches': matches,
            'leagues': leagues,
        })
        return context

    @staticmethod
    def get_team_matches(team):
        """
        Retrieve matches where the team participates.
        """
        return Match.active_objects().filter(
            Q(radiant_team_id=team.id) | Q(dire_team_id=team.id)
        )

    @staticmethod
    def get_team_leagues(team):
        """
        Retrieve leagues where the team participates.
        """
        return League.active_objects().filter(
            Q(series__team_one_id=team.id) | Q(series__team_two_id=team.id)
        ).distinct()


# Create an instance of TeamDetailView for URL routing
team_detail_view = TeamDetailView.as_view()


@csrf_protect
@require_POST
def update_team_data(request, team_id):
    if not team_id:
        messages.error(request, "Team ID is required.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    try:
        Team.objects.get_or_create(id=team_id)
        current_app.send_task("dj.teams.tasks.get_and_save_team_data", args=[team_id])
        messages.success(request, 'Task "Update Team Data" is running!')
    except Team.DoesNotExist:
        messages.error(request, "Team not found.")
    except Exception as e:
        messages.error(request, f"Exception occurred: {str(e)}")

    return redirect(f"/teams/{team_id}/")


@csrf_protect
@require_POST
def get_teams(request):
    try:
        current_app.send_task(name="dj.teams.tasks.task_get_and_save_teams_list")
        messages.success(request, 'Task "Update Teams" is running!')
    except Exception as e:
        messages.error(
            request,
            f'Exception occurred while running the task "Update Teams": {str(e)}',
        )
    return redirect("/teams/")
