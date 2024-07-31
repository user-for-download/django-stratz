import logging

from celery import shared_task

from dj.common.utils import process_entities
from dj.matches.services import save_match_data, fetch_matches, fetch_and_process_match

logger = logging.getLogger(__name__)


@shared_task()
def save_match_from_data(match):
    try:
        save_match_data(match)
    except Exception as e:
        return f"Error saving match: {str(e)}"


@shared_task()
def task_get_and_save_match(match_id: int):
    try:
        fetch_and_process_match(match_id)
    except Exception as e:
        return f"Error k_get_and_save_match: {str(e)}"


@shared_task()
def task_get_and_save_object_matches(obj_type: str, obj_id: int):
    try:
        matches_qs = fetch_matches(obj_id, obj_type)
        logger.info("matches count: %s", matches_qs.count())
        process_entities(matches_qs, task_get_and_save_match, 'match')
    except Exception as e:
        return f"Error task_get_and_save_series_matches: {str(e)}"
