import logging

from celery import shared_task

from dj.common.utils import process_entities
from dj.teams.models import Team
from dj.teams.services import get_and_save_team, fetch_and_process_teams

logger = logging.getLogger(__name__)


@shared_task
def task_get_and_save_teams_list():
    try:
        fetch_and_process_teams()
    except Exception as e:
        logger.exception(f'Exception in task_get_and_save_teams_list: {repr(e)}')


@shared_task
def get_and_save_team_data(team_id: int):
    """Fetches and updates pro players."""
    try:
        get_and_save_team(team_id)
    except Exception as e:
        logger.exception(f'Exception in task_get_and_save_team: {repr(e)}')


@shared_task()
def check_and_save_pro_teams():
    try:
        process_entities(Team.objects.is_pro(), get_and_save_team_data, 'Team')
    except Exception as e:
        logger.error("Failed to task_get_and_update_pro_teams: %s", e)
