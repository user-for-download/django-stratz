import logging

from celery import shared_task

from .models import Player
from .services import get_and_save_player, fetch_and_process_pro_players
from ..common.utils import process_entities
from ..teams.services import update_team_in_players

logger = logging.getLogger(__name__)


@shared_task
def task_get_and_save_pro_players_list():
    """Fetches and updates pro players."""
    try:
        fetch_and_process_pro_players()
        # update_team_in_players()
    except Exception as e:
        logger.exception(f'Exception in get_pro_players: {repr(e)}')


@shared_task
def get_and_save_player_data(player_id: int):
    """Fetches and updates a specific pro player by their ID."""
    try:
        get_and_save_player(player_id)
    except Exception as e:
        logger.exception(f'Exception in task_get_and_save_player: {repr(e)}')


@shared_task()
def check_and_save_pro_players():
    try:
        process_entities(Player.objects.pro_player(), get_and_save_player_data, 'Player')
    except Exception as e:
        # Logging error in case of an exception
        logger.error("Failed to check_and_save_pro_players: %s", e)
