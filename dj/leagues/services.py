import logging
from typing import Optional, Any, Dict

from django.db import transaction

from dj.common.urls import get_url_league_list, get_url_league_match_list, get_url_league_series_list
from dj.common.utils import response_to_json, to_abs, datetime_to_int
from .models import League, Series
from .schemas import SCHEMA_LEAGUE_LIST, SCHEMA_LEAGUE_SERIES_LIST
from ..common.constants import LEAGUE_LIST_COUNT
from ..matches.tasks import save_match_from_data
from ..teams.models import Team

logger = logging.getLogger(__name__)


def get_and_save_league_matches(league_id: int) -> None:
    try:
        league, _ = League.objects.get_or_create(id=league_id)
        url = get_url_league_match_list(league_id, 300, 0)
        response = response_to_json(url, {})
        # response = load_json('dj/common/json/pgl-matches.json')
        matches_list = response if isinstance(response, list) else []
        for match in matches_list:
            save_match_from_data.delay(match)
    except Exception as e:
        logger.error(f"get_and_save_league_series: An error occurred: {e}")


def get_and_save_league_series(league_id: int, force: bool = False) -> None:
    try:
        league, _ = League.objects.get_or_create(id=league_id)
        url = get_url_league_series_list(league_id, 300, 0)
        response = response_to_json(url, SCHEMA_LEAGUE_SERIES_LIST)
        # response = load_json('dj/common/json/series.json')
        series_list = response if isinstance(response, list) else []

        for series_data in series_list:
            series, _ = Series.objects.get_or_create(id=series_data.get('id'))
            is_need = series_data.get('lastMatchDate') >= datetime_to_int(series.updated_at)
            if force or is_need:
                save_series_data(series_data)
    except Exception as e:
        logger.error(f"get_and_save_league_series: An error occurred: {e}")


def save_series_data(series_data: Dict[str, Any]) -> None:
    try:
        save_series(series_data)
        for match_data in series_data['matches']:
            if int(match_data.get('id')) > 7833796201:
                save_match_from_data.delay(match_data)
    except Exception as e:
        logger.error(f"process_series_data: Error processing series data: {e}")


def save_series(series_data: Dict[str, Any]) -> Optional[Series]:
    try:
        team_one_id = to_abs(series_data, 'teamOneId')
        team_two_id = to_abs(series_data, 'teamTwoId')
        team_one, _ = Team.objects.get_or_create(id=team_one_id)
        team_two, _ = Team.objects.get_or_create(id=team_two_id)
        instance, _ = Series.objects.update_or_create(
            id=series_data.get('id'),
            defaults={
                'league_id': series_data.get('leagueId'),
                'team_two': team_two,
                'team_one': team_one,
                'type': series_data.get('type'),
                'team_one_win_count': series_data.get('teamOneWinCount'),
                'team_two_win_count': series_data.get('teamTwoWinCount'),
                'winning_team_id': to_abs(series_data, 'winningTeamId'),
                'last_match_date_time': series_data.get('lastMatchDate'),
            }
        )
        return instance
    except Exception as e:
        logger.error(f'Failed to save Series: {e}')
        return None


def save_league(league_data: Dict[str, Any]) -> Optional[League]:
    """
    Save or update a league record in the database.
    """
    try:
        instance, _ = League.objects.update_or_create(
            id=league_data.get('id'),
            defaults={
                'registration_period': league_data.get('registrationPeriod'),
                'country': league_data.get('country'),
                'venue': league_data.get('venue'),
                'private': league_data.get('private'),
                'city': league_data.get('city'),
                'description': league_data.get('description'),
                'has_live_matches': league_data.get('hasLiveMatches'),
                'tier': league_data.get('tier'),
                'tournament_url': league_data.get('tournamentUrl'),
                'free_to_spectate': league_data.get('freeToSpectate'),
                'is_followed': league_data.get('isFollowed'),
                'pro_circuit_points': league_data.get('proCircuitPoints'),
                'banner': league_data.get('banner'),
                'stop_sales_time': league_data.get('stopSalesTime'),
                'image_uri': league_data.get('imageUri'),
                'display_name': league_data.get('displayName'),
                'end_datetime': league_data.get('endDateTime'),
                'name': league_data.get('name'),
                'prize_pool': league_data.get('prizePool'),
                'base_prize_pool': league_data.get('basePrizePool'),
                'region': league_data.get('region'),
                'start_datetime': league_data.get('startDateTime'),
                'status': league_data.get('status'),
            }
        )
        return instance
    except Exception as e:
        logger.error(f'An error occurred while saving League: {e}')
        return None


@transaction.atomic
def fetch_and_process_leagues() -> None:
    """
    Fetch and process league data from the external API.
    """
    try:
        url = get_url_league_list(take=LEAGUE_LIST_COUNT, order_by='-startDateTime')
        response = response_to_json(url, SCHEMA_LEAGUE_LIST)
        tournaments = response if isinstance(response, list) else []
        for league_data in tournaments:
            save_league(league_data)
        League.objects.update_is_over()
    except Exception as e:
        logger.error(f"fetch_and_process_leagues: An error occurred during the transaction: {e}")
