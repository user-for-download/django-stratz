import logging
from typing import Optional, Any, Dict

from django.db import transaction

from dj.common.utils import response_to_json, save_data_if_exists, process_related_data
from .models import (
    SteamAccount, ProSteamAccount, PlayerBadge, Player, SeasonRank, PlayerName, BattlePass, TeamMember
)
from .schemas import SCHEMA_PLAYERS
from ..common.urls import get_url_pro_steam_acc, get_url_player
from ..teams.services import save_team

logger = logging.getLogger(__name__)


def save_pro_steam_account(pro_data: Dict[str, Any]) -> Optional[ProSteamAccount]:
    try:
        instance, _ = ProSteamAccount.objects.update_or_create(
            steam_account_id=pro_data.get('steamAccountId'),
            defaults={
                'name': pro_data.get('name'),
                'real_name': pro_data.get('realName'),
                'fantasy_role': pro_data.get('fantasyRole'),
                'team_id': pro_data.get('teamId'),
                'sponsor': pro_data.get('sponsor'),
                'is_locked': pro_data.get('isLocked'),
                'is_pro': pro_data.get('isPro'),
                'total_earnings': pro_data.get('totalEarnings'),
                'birthday': pro_data.get('birthday'),
                'romanized_real_name': pro_data.get('romanizedRealName'),
                'roles': pro_data.get('roles'),
                'statuses': pro_data.get('statuses'),
                'countries': pro_data.get('countries'),
                'aliases': pro_data.get('aliases'),
                'ti_wins': pro_data.get('tiWins'),
                'is_ti_winner': pro_data.get('istiwinner'),
                'position': pro_data.get('position'),
                'twitter_link': pro_data.get('twitterLink'),
                'twitch_link': pro_data.get('twitchLink'),
                'instagram_link': pro_data.get('instagramLink'),
                'vk_link': pro_data.get('vkLink'),
                'you_tube_link': pro_data.get('youTubeLink'),
                'facebook_link': pro_data.get('facebookLink'),
                'weibo_link': pro_data.get('weiboLink'),
                'signature_heroes': pro_data.get('signatureHeroes'),
            }
        )
        return instance
    except Exception as e:
        logger.error("Failed to save pro steam account: %s", e)
        return None


def save_steam_account(account_data: Dict[str, Any]) -> Optional[SteamAccount]:
    try:
        acc_id = account_data.get('id')
        instance, _ = SteamAccount.objects.update_or_create(
            id=acc_id,
            defaults={
                'last_active_time': account_data.get('lastActiveTime'),
                'pro_steam_account_id': acc_id,
                'profile_uri': account_data.get('profileUri'),
                'real_name': account_data.get('realName'),
                'time_created': account_data.get('timeCreated'),
                'country_code': account_data.get('countryCode'),
                'state_code': account_data.get('stateCode'),
                'city_id': account_data.get('cityId'),
                'community_visible_state': account_data.get('communityVisibleState'),
                'name': account_data.get('name'),
                'avatar': account_data.get('avatar'),
                'primary_clan_id': account_data.get('primaryClanId'),
                'solo_rank': account_data.get('soloRank'),
                'party_rank': account_data.get('partyRank'),
                'is_dota_plus_subscriber': account_data.get('isDotaPlusSubscriber', False),
                'dota_plus_original_start_date': account_data.get('dotaPlusOriginalStartDate'),
                'is_anonymous': account_data.get('isAnonymous', False),
                'is_stratz_public': account_data.get('isStratzPublic', False),
                'season_rank': account_data.get('seasonRank'),
                'season_leaderboard_rank': account_data.get('seasonLeaderboardRank'),
                'season_leaderboard_division_id': account_data.get('seasonLeaderboardDivisionId'),
                'smurf_flag': account_data.get('smurfFlag', False),
                'smurf_check_date': account_data.get('smurfCheckDate'),
                'last_match_date_time': account_data.get('lastMatchDateTime'),
                'last_match_region_id': account_data.get('lastMatchRegionId'),
                'dota_account_level': account_data.get('dotaAccountLevel'),
                'rank_shift': account_data.get('rankShift', 0)
            }
        )
        return instance
    except Exception as e:
        logger.error("Failed to save steam account: %s", e)
        return None


def save_badge(badge_data: Dict[str, Any], player: Player) -> Optional[PlayerBadge]:
    try:
        instance, _ = player.badges.update_or_create(
            badge_id=badge_data.get('badgeId'),
            defaults={
                'steam_id': badge_data.get('steamId'),
                'created_date_time': badge_data.get('createdDateTime'),
                'slot': badge_data.get('slot'),
            }
        )
        return instance
    except Exception as e:
        logger.error("Failed to save player badge: %s", e)
        return None


def save_battle_pass(battle_pass_data: Dict[str, Any], player: Player) -> Optional[BattlePass]:
    try:
        instance, _ = player.battle_pass.update_or_create(
            event_id=battle_pass_data.get('eventId'),
            defaults={
                'level': battle_pass_data.get('level'),
                'country_code': battle_pass_data.get('countryCode'),
                'bracket': battle_pass_data.get('bracket'),
                'is_anonymous': battle_pass_data.get('isAnonymous')
            }
        )
        return instance
    except Exception as e:
        logger.error("Failed to save steam account battle pass: %s", e)
        return None


def save_season_rank(rank_data: Dict[str, Any], player: Player) -> Optional[SeasonRank]:
    try:
        instance, _ = player.ranks.update_or_create(
            season_rank_id=rank_data.get('seasonRankId'),
            defaults={
                'as_of_date_time': rank_data.get('asOfDateTime'),
                'rank': rank_data.get('rank'),
                'is_core': rank_data.get('isCore')
            }
        )
        return instance
    except Exception as e:
        logger.error("Failed to save steam account season rank: %s", e)
        return None


def save_player(player_data: Dict[str, Any]) -> Optional[Player]:
    """
    Save or update a player record in the database.
    """
    try:
        player_id = player_data.get('steamAccountId')
        instance, _ = Player.objects.update_or_create(
            id=player_id,
            defaults={
                'steam_account_id': player_id,
                'last_match_date': player_data.get('date'),
                'last_region_id': player_data.get('lastRegionId'),
                'first_match_date': player_data.get('firstMatchDate'),
                'match_count': player_data.get('matchCount'),
                'win_count': player_data.get('winCount'),
                'behavior_score': player_data.get('behaviorScore'),
                'is_followed': player_data.get('isFollowed', False),
                'is_favorite': player_data.get('isFavorite', False),
                'language_codes': player_data.get('languageCode', []),
            }
        )
        return instance
    except Exception as e:
        logger.error(f'An error occurred while saving Player: {e}')
        return None


def save_player_name(name_data: Dict[str, Any], player: Player) -> Optional[PlayerName]:
    try:
        instance, _ = player.names.update_or_create(
            name=name_data.get('name'),
            defaults={
                'last_seen_date_time': name_data.get('lastseendatetime')
            }
        )
        return instance
    except Exception as e:
        logger.error("Failed to save player name: %s", e)
        return None


def save_player_instance(player_id) -> Optional[Player]:
    try:
        steam_account, _ = SteamAccount.objects.get_or_create(id=player_id)
        pro_steam_account, _ = ProSteamAccount.objects.get_or_create(steam_account_id=player_id)
        player, _ = Player.objects.get_or_create(id=player_id, defaults={'steam_account': steam_account})
        return player
    except Exception as e:
        logger.error("Failed to save player instance: %s", e)
        return None


@transaction.atomic
def get_and_save_player(player_id: int) -> Optional[Player]:
    try:
        response = response_to_json(get_url_player(player_id), SCHEMA_PLAYERS)
        # response = load_json('dj/common/json/pl-1.json')
        player_data = response if isinstance(response, dict) else {}

        steam_data = player_data.get('steamAccount')

        save_player_instance(player_id)

        save_data_if_exists(steam_data, 'proSteamAccount', save_pro_steam_account)

        save_data_if_exists(player_data, 'steamAccount', save_steam_account)

        player = save_player(player_data)

        team_data = player_data.get('team')
        if team_data:
            save_data_if_exists(team_data, 'team', save_team)
            team_member, _ = TeamMember.objects.update_or_create(
                steam_account_id=steam_data.get('id'),
                team_id=team_data.get('teamId'),
                defaults={
                    "first_match_id": team_data.get("firstMatchId"),
                    "first_match_date_time": team_data.get("firstMatchDateTime"),
                    "last_match_id": team_data.get("lastMatchId"),
                    "last_match_date_time": team_data.get("lastMatchDateTime"),
                },
            )
            player.team = team_member
            player.save()
        if player:
            process_related_data(player_data, 'battlePass', save_battle_pass, player)
            process_related_data(player_data, 'badges', save_badge, player)
            process_related_data(player_data, 'ranks', save_season_rank, player)
            process_related_data(player_data, 'names', save_player_name, player)
        return player
    except Exception as e:
        logger.error("Failed to save player: %s", e)


@transaction.atomic
def fetch_and_process_pro_players() -> None:
    try:
        pro_players = response_to_json(get_url_pro_steam_acc(), {})
        for player_id, player_data in pro_players.items():
            pro_steam_account = save_pro_steam_account(player_data)
            if pro_steam_account:
                steam_account, _ = pro_steam_account.steam_account.update_or_create(
                    id=player_id,
                    defaults={
                        'real_name': player_data.get('realName'),
                        'name': player_data.get('name'),
                    }
                )
                if steam_account:
                    Player.objects.update_or_create(id=player_id, defaults={
                        "steam_account": steam_account
                    })
    except Exception as e:
        logger.error("Failed to save pro players: %s", e)
