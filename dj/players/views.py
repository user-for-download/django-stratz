from celery import current_app
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from dj.players.models import Player
from dj.players.models import SteamAccount


class PlayerListView(ListView):
    model = Player
    paginate_by = 25

    def get_queryset(self):
        return Player.objects.pro_player()


player_list_view = PlayerListView.as_view()


class PlayerDetailView(DetailView):
    model = Player
    slug_field = "id"
    slug_url_kwarg = "player_id"


player_detail_view = PlayerDetailView.as_view()


@csrf_protect
@require_POST
def get_players(request):
    try:
        current_app.send_task(name="dj.players.tasks.task_get_and_save_pro_players_list")
        messages.success(request, 'Task "Update Players" is running!')
    except Exception as e:
        messages.error(
            request,
            f'Exception occurred while running the task "Update Players": {str(e)}',
        )
    return redirect("/players/")


@csrf_protect
@require_POST
def update_player_data(request, player_id):
    if not player_id:
        messages.error(request, "Account ID is required.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    try:
        current_app.send_task(
            "dj.players.tasks.get_and_save_player_data", args=[player_id]
        )
        messages.success(request, 'Task "Update Player Data" is running!')
    except SteamAccount.DoesNotExist:
        messages.error(request, "Player not found.")
    except Exception as e:
        messages.error(request, f"Exception occurred: {str(e)}")

    return redirect(f"/players/{player_id}/")
