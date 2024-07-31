import logging
from datetime import timedelta

from orjson import orjson

from dj.common.constants import PLAYER, LEAGUE, TEAM
from dj.common.utils import now_tz
from dj.leagues.models import League
from dj.matches.services import get_hero_data, get_hero_data_for_player
from dj.players.models import Player
from dj.teams.models import Team

logger = logging.getLogger(__name__)

TOP = 30


def update_popular_picks_bans(entity_id: int, entity_type: str) -> None:
    """
    Update the popular hero picks and bans for a given entity.

    :param entity_id: ID of the entity (player, league, or team)
    :param entity_type: Type of the entity ('PLAYER', 'LEAGUE', or 'TEAM')
    """
    try:
        # Determine data source based on entity type
        if entity_type == PLAYER:
            data = get_hero_data_for_player(entity_id)
            entity = Player.objects.get(id=entity_id)
        else:
            data = get_hero_data(entity_id, entity_type)
            if entity_type == LEAGUE:
                entity = League.objects.get(id=entity_id)
            elif entity_type == TEAM:
                entity = Team.objects.get(id=entity_id)
            else:
                logger.info(f"update_popular_picks_bans EMPTY: {entity_type} ID: {entity_id}")
                return

        # Extract picks and bans from data
        nodes_picks = data.get('nodes_picks', [])
        nodes_bans = data.get('nodes_bans', [])
        picks = orjson.dumps(nodes_picks[:TOP]).decode('utf-8')
        bans = orjson.dumps(nodes_bans[:TOP]).decode('utf-8')

        # Check if last update was within the last 24 hours
        last = entity.pick_bans.order_by('-time_stamp_at').last()
        if last and (now_tz() - last.time_stamp_at) <= timedelta(hours=24):
            logger.info(f"update_popular_picks_bans time_stamp_at < 24 hours: {entity_type} ID: {entity_id}")
            return

        # Update or create new pick_bans entry
        entity.pick_bans.update_or_create(
            defaults={
                'entity_type': entity_type,
                'entity_id': entity_id,
                'hero_picks': picks,
                'hero_bans': bans
            }
        )
    except Exception as e:
        logger.exception(f"update_popular_picks_bans: {entity_type} ID: {entity_id} %s", e)
