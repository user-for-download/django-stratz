import logging
from typing import Optional, Any, Dict

from django.db import transaction

from dj.common.urls import get_opendota_teams, get_url_team
from dj.common.utils import response_to_json, process_related_data
from dj.players.models import Player, TeamMember, SteamAccount
from dj.teams.models import Team
from dj.teams.schemas import SCHEMA_TEAM

logger = logging.getLogger(__name__)


@transaction.atomic
def get_and_save_team(team_id: int) -> None:
    try:
        response = response_to_json(get_url_team(team_id), SCHEMA_TEAM)
        # response = load_json('dj/common/json/team-s.json')
        team_data = response if isinstance(response, dict) else {}
        team = save_team(team_data)
        process_related_data(team_data, 'members', save_team_member, team)
        members = team.members.active().order_by('-last_match_id')
        for member in members[:5]:
            Player.objects.update_or_create(id=member.steam_account.id, defaults={
                "team": member
            })
    except Exception as e:
        logger.error(
            f"fetch_and_process_team: An error occurred during the transaction: {e}"
        )


def save_team_member(member_data: Dict[str, Any], team: Team) -> Optional[TeamMember]:
    try:
        steam_account_id = member_data.get("steamAccount", {}).get("id")
        SteamAccount.objects.get_or_create(id=steam_account_id)
        team_member, _ = team.members.update_or_create(
            steam_account_id=steam_account_id,
            defaults={
                "first_match_id": member_data.get("firstMatchId"),
                "first_match_date_time": member_data.get("firstMatchDateTime"),
                "last_match_id": member_data.get("lastMatchId"),
                "last_match_date_time": member_data.get("lastMatchDateTime"),
            },
        )
        return team_member
    except Exception as e:
        logger.error(f"Failed to save_team_members: {e}")
        return None


def save_team(team_data: Dict[str, Any]) -> Optional[Team]:
    try:
        defaults = {
            "name": team_data.get("name"),
            "tag": team_data.get("tag"),
            "date_created": team_data.get("dateCreated"),
            "is_pro": team_data.get("isProfessional"),
            "logo": team_data.get("logo"),
            "banner_logo": team_data.get("bannerLogo"),
            "win_count": team_data.get("winCount"),
            "loss_count": team_data.get("lossCount"),
            "last_match_date_time": team_data.get("lastMatchDateTime"),
            "is_followed": team_data.get("isFollowed"),
            "country_name": team_data.get("countryName", ""),
        }
        rank = team_data.get("rank")
        if rank:
            defaults["rank"] = rank
        team, _ = Team.objects.update_or_create(id=team_data.get("id"), defaults=defaults)
        return team
    except Exception as e:
        logger.error(f"Failed to save team: {e}")
        return None


def update_team_in_players() -> None:
    try:
        steam_acc_list = (
            TeamMember.objects.filter(team__is_pro=True)
            .order_by("last_match_id")
            .distinct()
        )

        with transaction.atomic():
            for acc in steam_acc_list:
                Player.objects.update_or_create(
                    steam_account=acc.steam_account, defaults={"team": acc}
                )

        logger.info("Successfully updated pro team members")
    except Exception as e:
        logger.error(f"An error occurred in get_and_save_pro_team_members: {e}")


@transaction.atomic
def fetch_and_process_teams() -> None:
    try:
        response = response_to_json(get_opendota_teams(), {})
        response_data = response if isinstance(response, dict) else {}
        teams = response_data.get("rows")
        for team in list(teams):
            try:
                is_pro = True if team.get("rating") >= 1200 else False
                team_data = {
                    "id": team.get("team_id"),
                    "name": team.get("name"),
                    "tag": team.get("tag"),
                    "isProfessional": is_pro,
                    "logo": team.get("logo_url"),
                    "rank": team.get("rating"),
                    "banner_logo": team.get("bannerLogo"),
                    "winCount": team.get("wins"),
                    "lossCount": team.get("losses"),
                    "lastMatchDateTime": team.get("last_match_time"),
                }
                save_team(team_data)
            except Exception as e:
                logger.exception(f"An error occurred: {e}")
    except Exception as e:
        logger.error(
            f"fetch_and_process_teams: An error occurred during the transaction: {e}"
        )
