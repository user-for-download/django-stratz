import logging

from celery import shared_task

from dj.common.constants import LEAGUE, TEAM, PLAYER
from dj.common.utils import process_entities
from dj.leagues.models import League
from dj.players.models import Player
from dj.stats.services import update_popular_picks_bans
from dj.teams.models import Team

logger = logging.getLogger(__name__)


@shared_task
def task_update_popular_picks_bans(entity_id: int, entity_type: str) -> None:
    try:
        update_popular_picks_bans(entity_id, entity_type)
    except Exception as e:
        logger.exception(f"task_get_and_save: {entity_type} ID: {entity_id} %s", e)


@shared_task
def task_get_popular_picks_bans_leagues() -> None:
    process_entities(League.objects.tier2(), lambda id: task_update_popular_picks_bans(id, LEAGUE), 'League')


@shared_task
def task_get_popular_picks_bans_teams() -> None:
    process_entities(Team.objects.is_pro(), lambda id: task_update_popular_picks_bans(id, TEAM), 'Team')


@shared_task
def task_get_popular_picks_bans_players() -> None:
    process_entities(Player.objects.pro_player(), lambda id: task_update_popular_picks_bans(id, PLAYER), 'Player')
