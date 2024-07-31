import logging

from celery import shared_task

from .models import League, Series
from .services import fetch_and_process_leagues, get_and_save_league_series, get_and_save_league_matches
from ..common.utils import process_entities

logger = logging.getLogger(__name__)


@shared_task
def task_get_and_save_leagues_list():
    try:
        fetch_and_process_leagues()
    except Exception as e:
        logger.exception(f'Exception in task_get_and_save_leagues_list: {repr(e)}')


@shared_task
def task_get_and_save_league_matches(league_id: int):
    try:
        get_and_save_league_matches(league_id)
    except Exception as e:
        logger.exception(f'Exception in task_get_and_save_league_matches: {repr(e)}')


@shared_task
def task_get_and_save_league_series(league_id: int, force: bool = False) -> None:
    try:
        get_and_save_league_series(league_id, force)
    except Exception as e:
        logger.exception(f'Exception in task_get_and_save_league_series: {repr(e)}')


@shared_task()
def check_and_save_leagues_data():
    try:
        League.objects.update_is_over()
        Series.objects.update_is_over()
        process_entities(League.objects.tier2(), task_get_and_save_league_series, 'League')
    except Exception as e:
        logger.exception("Failed to check_and_save_leagues_data: %s", e)
