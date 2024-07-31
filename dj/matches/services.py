import logging
from collections import Counter
from itertools import combinations
from typing import Dict, Any, Optional, Union, List, Tuple

from django.db import transaction
from django.db.models import Q, Model, Subquery, QuerySet

from .models import (
    Match,
    MatchPlayer,
    MatchPickBan,
    CourierEvent,
    MatchPlaybackData,
    WardEvent,
    TowerDeathEvent,
    RoshanEvent,
    BuildingEvent,
    MatchRuneEvent,
)
from ..common.constants import TEAM
from ..common.urls import get_url_match
from ..common.utils import (
    get_hero_info,
    scale_size,
    process_related_data,
    to_abs, response_to_json, )
from ..players.services import save_player_instance

logger = logging.getLogger(__name__)


def fetch_matches(id_obj: int, obj: str, filters: Q = Q()) -> QuerySet:
    """
    Fetch matches based on the given object type and filters.

    :param id_obj: ID of the object (league, series, or team)
    :param obj: Type of the object ('league', 'series', 'team', or 'all')
    :param filters: Additional filters for querying matches
    :return: QuerySet of matches
    """
    match_filter_map = {
        "league": Q(league__id=id_obj),
        "series": Q(series__id=id_obj),
        "team": Q(radiant_team__id=id_obj) | Q(dire_team__id=id_obj),
        "all": Q(id__gte=1),
    }
    match_filter = match_filter_map.get(obj, lambda: Match.active_objects().filter(filters).order_by('-id')[:500])

    if callable(match_filter):
        matches = match_filter()
    else:
        matches = Match.active_objects().filter(match_filter & filters).order_by('-id')[:500]

    return matches.select_related("league", "series", "radiant_team", "dire_team").prefetch_related("pick_bans")


def process_heroes_1(matches: QuerySet, is_pick: bool = True) -> (Counter, List[Dict[str, int]]):
    hero_counts = Counter()
    links = []

    for match in matches:
        pick_bans = list(
            match.pick_bans.filter(is_pick=is_pick).values_list(
                "hero_id", flat=True
            )
        )
        hero_counts.update(pick_bans)
        links.extend(
            {"source": hero_id, "target": target_hero_id}
            for i, hero_id in enumerate(pick_bans)
            for target_hero_id in pick_bans[i + 1:]
        )

    return hero_counts, links


def combinations_hero(hero_list: List[int]) -> List[Dict[str, int]]:
    """
    Generate all unique combinations of hero pairs from a list of heroes.

    :param hero_list: List of hero IDs
    :return: List of dictionaries with hero combinations
    """
    try:
        return [{"source": s[0], "target": s[1]} for s in combinations(hero_list, 2)]
    except Exception as e:
        logger.exception(f'Exception in combinations_hero: {repr(e)}')
        return []


def process_heroes(matches: QuerySet, id_obj: int = 0, obj: str = "") -> Tuple[
    Counter, List[Dict[str, int]], Counter, List[Dict[str, int]]]:
    """
    Process heroes from the given matches to count picks and bans.

    :param matches: QuerySet of matches
    :param id_obj: ID of the object (team if applicable)
    :param obj: Type of the object ('team' if applicable)
    :return: Tuple containing hero pick counts, pick links, hero ban counts, and ban links
    """
    hero_counts_picks = Counter()
    links_picks = []
    hero_counts_bans = Counter()
    links_bans = []

    for match in matches:
        picks = []
        bans = []

        # Filter pick_bans based on the team if the object is TEAM
        qs_list = match.pick_bans.filter(
            is_radiant=(id_obj == match.radiant_team_id)
        ) if obj == TEAM else match.pick_bans

        for pick_ban in qs_list.values("hero_id", "is_pick"):
            hero_id = pick_ban['hero_id']
            if pick_ban['is_pick']:
                picks.append(hero_id)
            else:
                bans.append(hero_id)

        hero_counts_picks.update(picks)
        hero_counts_bans.update(bans)

        links_picks.extend(combinations_hero(picks))
        links_bans.extend(combinations_hero(bans))

    return hero_counts_picks, links_picks, hero_counts_bans, links_bans


def process_player_heroes(player_id: int, filters: Q = Q()) -> Counter:
    hero_counts = Counter()
    player_matches = Match.active_objects().filter(
        id__in=Subquery(
            MatchPlayer.active_objects()
            .filter(steam_account__id=player_id)
            .values('match_id')
        )
    ).filter(filters)

    for match in player_matches:
        hero_ids = list(
            match.players.active().filter(
                steam_account__id=player_id
            ).values_list(
                "hero_id", flat=True
            )
        )
        hero_counts.update(hero_ids)

    return hero_counts


def create_node(hero_id: int, count: int, min_count: int, max_count: int) -> Dict[str, Any]:
    hero_name, hero_image = get_hero_info(hero_id)
    return {
        "id": hero_id,
        "name": hero_name,
        "count": count,
        "image": hero_image,
        "size": scale_size(count, min_count, max_count),
    }


def get_hero_data(
    id_obj: int, obj: str = "", filters: Q = Q()
) -> Dict[str, Union[List[Dict[str, Any]], List[Dict[str, int]]]]:
    matches_list = fetch_matches(id_obj, obj, filters)

    hero_counts_picks, links_picks, hero_counts_bans, links_bans = process_heroes(matches_list, id_obj, obj)

    min_count_picks = min(hero_counts_picks.values(), default=0)
    max_count_picks = max(hero_counts_picks.values(), default=100)
    min_count_bans = min(hero_counts_bans.values(), default=0)
    max_count_bans = max(hero_counts_bans.values(), default=100)

    nodes_picks = [
        create_node(hero_id, count, min_count_picks, max_count_picks)
        for hero_id, count in hero_counts_picks.items()
    ]
    nodes_bans = [
        create_node(hero_id, count, min_count_bans, max_count_bans)
        for hero_id, count in hero_counts_bans.items()
    ]

    return {
        "nodes_picks": nodes_picks,
        "links_picks": links_picks,
        "nodes_bans": nodes_bans,
        "links_bans": links_bans,
    }


def get_hero_data_for_player(player_id: int, filters: Q = Q()) -> Dict[str, Any]:
    hero_counts = process_player_heroes(player_id, filters)

    min_count_picks = min(hero_counts.values(), default=0)
    max_count_picks = max(hero_counts.values(), default=100)

    nodes_picks = [
        create_node(hero_id, count, min_count_picks, max_count_picks)
        for hero_id, count in hero_counts.items()
    ]
    return {"nodes_picks": nodes_picks}


def fetch_and_process_match(match_id: int) -> None | Model:
    try:
        url = get_url_match(match_id)
        response = response_to_json(url, {})
        # response = load_json('dj/common/json/7833796201.json')
        match = response if isinstance(response, dict) else {}
        return save_match_data(match)
    except Exception as e:
        logger.error(f"fetch_and_process_match: An error occurred during the transaction: {e}")


def save_match_data(match_data: Dict[str, Any]) -> None | Model:
    try:
        if not match_data.get("endDateTime"):
            logger.error("save match MISSING endDateTime")
            return None

        match, _ = Match.objects.update_or_create(
            id=match_data.get("id"),
            defaults={
                "did_radiant_win": match_data.get("didRadiantWin", None),
                "duration_seconds": match_data.get("durationSeconds", None),
                "start_date_time": match_data.get("startDateTime", None),
                "tower_status_radiant": match_data.get("towerStatusRadiant", None),
                "tower_status_dire": match_data.get("towerStatusDire", None),
                "barracks_status_radiant": match_data.get(
                    "barracksStatusRadiant", None
                ),
                "barracks_status_dire": match_data.get("barracksStatusDire", None),
                "cluster_id": match_data.get("clusterId", None),
                "first_blood_time": match_data.get("firstBloodTime", None),
                "lobby_type": match_data.get("lobbyType", None),
                "num_human_players": match_data.get("numHumanPlayers", None),
                "game_mode": match_data.get("gameMode", None),
                "replay_salt": match_data.get("replaySalt", None),
                "is_stats": match_data.get("isStats", None),
                "tournament_id": match_data.get("tournamentId", None),
                "tournament_round": match_data.get("tournamentRound", None),
                "average_rank": match_data.get("averageRank", None),
                "actual_rank": match_data.get("actualRank", None),
                "average_imp": match_data.get("averageImp", None),
                "parsed_date_time": match_data.get("parsedDateTime", None),
                "stats_date_time": match_data.get("statsDateTime", None),
                "league_id": match_data.get("leagueId", None),
                "radiant_team_id": to_abs(match_data, 'radiantTeamId'),
                "dire_team_id": to_abs(match_data, 'direTeamId'),
                "series_id": match_data.get("seriesId", None),
                "game_version_id": match_data.get("gameVersionId", None),
                "region_id": match_data.get("regionId", None),
                "sequence_num": match_data.get("sequenceNum", None),
                "rank": match_data.get("rank", None),
                "bracket": match_data.get("bracket", None),
                "end_date_time": match_data.get("endDateTime", None),
                "actual_rank_weight": match_data.get("actualRankWeight", None),
                "analysis_outcome": match_data.get("analysisOutcome", None),
                "predicted_outcome_weight": match_data.get(
                    "predictedOutcomeWeight", None
                ),
                "bottom_lane_outcome": match_data.get("bottomLaneOutcome", None),
                "mid_lane_outcome": match_data.get("midLaneOutcome"),
                "top_lane_outcome": match_data.get("topLaneOutcome"),
                "radiant_networth_lead": match_data.get("radiantNetworthLead"),
                "radiant_experience_lead": match_data.get("radiantExperienceLead"),
                "radiant_kills": match_data.get("radiantKills"),
                "dire_kills": match_data.get("direKills"),
                "tower_status": match_data.get("towerStatus"),
                "lane_report": match_data.get("laneReport"),
                "win_rates": match_data.get("winRates"),
                "predicted_win_rates": match_data.get("predictedWinRates"),
                "tower_deaths": match_data.get("towerDeaths"),
                "chat_events": match_data.get("chatEvents"),
                "did_request_download": match_data.get("didRequestDownload"),
                "game_result": match_data.get("gameResult"),
            },
        )
        plb_data = match_data.get("playbackData")
        if plb_data:
            plb_instance = save_playback_data(plb_data, match_data.get("id"))
            match.playback_data = plb_instance
            match.save()

        process_related_data(match_data, "players", save_match_player, match)
        process_related_data(match_data, "pickBans", save_match_pick_ban, match)
        return match
    except Exception as e:
        logger.error("Unexpected error occurred while saving match: %s", e)


def save_courier_event(event_data: Dict[str, Any], plb: MatchPlaybackData) -> CourierEvent:
    try:
        instance, _ = plb.courier_events.update_or_create(
            id=event_data.get("id"),
            owner=event_data.get("owner"),
            is_radiant=event_data.get("isRadiant"),
        )
        process_related_data(event_data, "events", save_courier_event_event, instance)
        return instance

    except Exception as e:
        logger.error("save_courier_event error: %s", e)


def save_courier_event_event(event_data: Dict[str, Any], courier_event: CourierEvent):
    try:
        instance, _ = courier_event.events.update_or_create(
            time=event_data.get("time"),
            x=event_data.get("x"),
            y=event_data.get("y"),
            defaults={
                "hp": event_data.get("hp"),
                "is_flying": event_data.get("is_flying"),
                "respawn_time": event_data.get("respawn_time"),
                "item0Id": event_data.get("item0Id"),
                "item1Id": event_data.get("item1Id"),
                "item2Id": event_data.get("item2Id"),
                "item3Id": event_data.get("item3Id"),
                "item4Id": event_data.get("item4Id"),
                "item5Id": event_data.get("item5Id"),
            },
        )
        return instance
    except Exception as e:
        logger.error("save_courier_event_event error: %s", e)


def save_rune_events(event_data: Dict[str, Any], plb: MatchPlaybackData) -> MatchRuneEvent:
    try:
        instance, _ = plb.rune_events.update_or_create(
            id=event_data.get("id"),
            time=event_data.get("time"),
            action=event_data.get("action"),
            defaults={
                "x": event_data.get("x"),
                "y": event_data.get("y"),
                "location": event_data.get("location"),
                "rune_type": event_data.get("runeType"),
            },
        )
        return instance
    except Exception as e:
        logger.error("save_rune_events error: %s", e)


def save_ward_events(event_data: Dict[str, Any], plb: MatchPlaybackData) -> WardEvent:
    try:
        instance, _ = plb.ward_events.update_or_create(
            id=event_data.get("id"),
            time=event_data.get("time"),
            action=event_data.get("action"),
            defaults={
                "from_player": event_data.get("fromPlayer"),
                "x": event_data.get("x"),
                "y": event_data.get("y"),
                "ward_type": event_data.get("wardType"),
                "player_destroyed": event_data.get("playerDestroyed"),
            },
        )
        return instance
    except Exception as e:
        logger.error("save_ward_events error: %s", e)


def save_tower_death_events(event_data: Dict[str, Any], plb: MatchPlaybackData) -> TowerDeathEvent:
    try:
        instance, _ = plb.tower_death_events.update_or_create(
            radiant=event_data.get("radiant"),
            dire=event_data.get("dire"),
            time=event_data.get("time"),
        )
        return instance
    except Exception as e:
        logger.error("save_tower_death_events error: %s", e)


def save_roshan_events(event_data: Dict[str, Any], plb: MatchPlaybackData) -> RoshanEvent:
    try:
        instance, _ = plb.roshan_events.update_or_create(
            time=event_data.get("time"),
            hp=event_data.get("hp"),
            item0=event_data.get("item0"),
            max_hp=event_data.get("maxHp"),
            x=event_data.get("x"),
            y=event_data.get("y"),
        )
        return instance
    except Exception as e:
        logger.error("save_roshan_events error: %s", e)


def save_building_events(event_data: Dict[str, Any], plb: MatchPlaybackData) -> BuildingEvent:
    try:
        instance, _ = plb.building_events.update_or_create(
            id=event_data.get("id"),
            time=event_data.get("time"),
            npc_id=event_data.get("npcId"),
            defaults={
                "type": event_data.get("type"),
                "hp": event_data.get("hp"),
                "max_hp": event_data.get("maxHp"),
                "x": event_data.get("x"),
                "y": event_data.get("y"),
                "is_radiant": event_data.get("isRadiant"),
            },
        )
        return instance
    except Exception as e:
        logger.error("save_building_events error: %s", e)


@transaction.atomic
def save_playback_data(plb_data: Dict[str, Any], match_id: int) -> Optional[MatchPlaybackData]:
    try:
        instance, _ = MatchPlaybackData.objects.get_or_create(
            match__id=match_id,
            radiant_captain_hero_id=plb_data.get("radiantCaptainHeroId"),
            dire_captain_hero_id=plb_data.get("direCaptainHeroId"),
        )
        process_related_data(plb_data, "runeEvents", save_rune_events, instance)
        # process_related_data(plb_data, "courierEvents", save_courier_event, instance)
        process_related_data(plb_data, "wardEvents", save_ward_events, instance)
        process_related_data(plb_data, "towerDeathEvents", save_tower_death_events, instance)
        process_related_data(plb_data, "roshanEvents", save_roshan_events, instance)
        process_related_data(plb_data, "buildingEvents", save_building_events, instance)
        return instance
    except Exception as e:
        logger.error("save_playback_data error: %s", e)
        return None


def save_match_pick_ban(pb_data: Dict[str, Any], match: Match) -> MatchPickBan:
    try:
        instance, _ = match.pick_bans.update_or_create(
            order=pb_data.get("order"),
            defaults={
                "is_pick": pb_data.get("isPick"),
                "hero_id": pb_data.get("heroId"),
                "banned_hero_id": pb_data.get("bannedHeroId"),
                "is_radiant": pb_data.get("isRadiant"),
                "player_index": pb_data.get("playerIndex"),
                "was_banned_successfully": pb_data.get("wasBannedSuccessfully"),
                "base_win_rate": pb_data.get("baseWinRate"),
                "adjusted_win_rate": pb_data.get("adjustedWinRate"),
                "pick_probability": pb_data.get("pickProbability"),
                "is_captain": pb_data.get("isCaptain"),
            },
        )
        return instance
    except Exception as e:
        logger.error("Failed to save match pick ban: %s", e)


def save_match_player(player_data: Dict[str, Any], match: Match) -> MatchPlayer:
    try:
        save_player_instance(player_data.get("steamAccountId"))
        instance, _ = match.players.update_or_create(
            steam_account_id=player_data.get("steamAccountId"),
            player_slot=player_data.get("playerSlot"),
            match_id=player_data.get("matchId"),
            hero_id=player_data.get("heroId"),
            defaults={
                "is_radiant": player_data.get("isRadiant"),
                "num_kills": player_data.get("numKills"),
                "num_deaths": player_data.get("numDeaths"),
                "num_assists": player_data.get("numAssists"),
                "leaver_status": player_data.get("leaverStatus"),
                "num_last_hits": player_data.get("numLastHits"),
                "num_denies": player_data.get("numDenies"),
                "gold_per_minute": player_data.get("goldPerMinute"),
                "experience_per_minute": player_data.get("experiencePerMinute"),
                "level": player_data.get("level"),
                "gold": player_data.get("gold"),
                "gold_spent": player_data.get("goldSpent"),
                "hero_damage": player_data.get("heroDamage"),
                "tower_damage": player_data.get("towerDamage"),
                "party_id": player_data.get("partyId"),
                "is_random": player_data.get("isRandom"),
                "lane": player_data.get("lane"),
                "streak_prediction": player_data.get("streakPrediction"),
                "intentional_feeding": player_data.get("intentionalFeeding"),
                "role": player_data.get("role"),
                "imp": player_data.get("imp"),
                "award": player_data.get("award"),
                "item0_id": player_data.get("item0Id"),
                "item1_id": player_data.get("item1Id"),
                "item2_id": player_data.get("item2Id"),
                "item3_id": player_data.get("item3Id"),
                "item4_id": player_data.get("item4Id"),
                "item5_id": player_data.get("item5Id"),
                "backpack0_id": player_data.get("backpack0Id"),
                "backpack1_id": player_data.get("backpack1Id"),
                "backpack2_id": player_data.get("backpack2Id"),
                "behavior": player_data.get("behavior"),
                "hero_healing": player_data.get("heroHealing"),
                "roam_lane": player_data.get("roamLane"),
                "is_victory": player_data.get("isVictory"),
                "networth": player_data.get("networth"),
                "neutral0_id": player_data.get("neutral0Id"),
                "dota_plus_hero_xp": player_data.get("dotaPlusHeroXp"),
                "invisible_seconds": player_data.get("invisibleSeconds"),
                "match_player_stats": player_data.get("matchPlayerStats"),
                "is_dire": player_data.get("isDire"),
                "role_basic": player_data.get("roleBasic"),
                "position": player_data.get("position"),
                "base_slot": player_data.get("baseSlot"),
                "kda": player_data.get("kda"),
                "map_location_home_fountain": player_data.get(
                    "mapLocationHomeFountain"
                ),
                "faction": player_data.get("faction"),
                "calculate_imp_lane": player_data.get("calculateImpLane"),
                "game_version_id": player_data.get("gameVersionId"),
                "stats": player_data.get("stats"),
                "playback_data": player_data.get("playbackData"),
                "abilities": player_data.get("abilities"),

            },
        )
        return instance
    except Exception as e:
        logger.error("Failed to save match player: %s", e)
