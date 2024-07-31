import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models

from dj.common.constants import HEROES
from dj.common.models import BaseModel, BaseManager
from dj.common.utils import unix_to_datetime, seconds_to_hours_minutes, sum_elements
from dj.leagues.models import League, Series
from dj.players.models import SteamAccount
from dj.teams.models import Team


class Event(BaseModel):
    time = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class MatchPickBanManager(BaseManager):
    def radiant_picks(self):
        return self.get_queryset().filter(is_radiant=True).filter(is_pick=True)

    def dire_picks(self):
        return self.get_queryset().filter(is_radiant=False).filter(is_pick=True)


class MatchPickBan(BaseModel):
    is_pick = models.BooleanField(blank=True, null=True)
    hero_id = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    banned_hero_id = models.IntegerField(blank=True, null=True)
    is_radiant = models.BooleanField(blank=True, null=True)
    player_index = models.IntegerField(blank=True, null=True)
    was_banned_successfully = models.BooleanField(blank=True, null=True)
    base_win_rate = models.IntegerField(blank=True, null=True)
    adjusted_win_rate = models.IntegerField(blank=True, null=True)
    pick_probability = models.IntegerField(blank=True, null=True)
    is_captain = models.BooleanField(blank=True, null=True)

    objects = MatchPickBanManager()

    @property
    def hero_image_url(self):
        url_image = "https://dj.binetc.site/static/images/heroes/npc_dota_hero_"
        hero_image_name = HEROES.get(self.hero_id, "default.png")
        return f"{url_image}{hero_image_name}"


class MatchPlayerSpectator(BaseModel):
    steam_id = models.IntegerField(blank=True, null=True)
    match_id = models.IntegerField(blank=True, null=True)
    is_radiant_coach = models.BooleanField(blank=True, null=True)
    is_victory = models.BooleanField(blank=True, null=True)


class MatchPlayerAdditionalUnit(BaseModel):
    match_id = models.PositiveBigIntegerField(blank=True, null=True)
    player_slot = models.IntegerField(blank=True, null=True)
    item0_id = models.IntegerField(blank=True, null=True)
    item1_id = models.IntegerField(blank=True, null=True)
    item2_id = models.IntegerField(blank=True, null=True)
    item3_id = models.IntegerField(blank=True, null=True)
    item4_id = models.IntegerField(blank=True, null=True)
    item5_id = models.IntegerField(blank=True, null=True)
    backpack0_id = models.IntegerField(blank=True, null=True)
    backpack1_id = models.IntegerField(blank=True, null=True)
    backpack2_id = models.IntegerField(blank=True, null=True)
    neutral0_id = models.IntegerField(blank=True, null=True)


class MatchPlayerAbility(Event):
    ability_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    game_version_id = models.IntegerField(blank=True, null=True)


class MatchPlayer(BaseModel):
    match_id = models.PositiveBigIntegerField(blank=True, null=True)
    player_slot = models.IntegerField(blank=True, null=True)
    hero_id = models.IntegerField(blank=True, null=True)
    is_radiant = models.BooleanField(blank=True, null=True)
    num_kills = models.IntegerField(blank=True, null=True)
    num_deaths = models.IntegerField(blank=True, null=True)
    num_assists = models.IntegerField(blank=True, null=True)
    leaver_status = models.IntegerField(blank=True, null=True)
    num_last_hits = models.IntegerField(blank=True, null=True)
    num_denies = models.IntegerField(blank=True, null=True)
    gold_per_minute = models.IntegerField(blank=True, null=True)
    experience_per_minute = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    gold = models.IntegerField(blank=True, null=True)
    gold_spent = models.IntegerField(blank=True, null=True)
    hero_damage = models.IntegerField(blank=True, null=True)
    tower_damage = models.IntegerField(blank=True, null=True)
    party_id = models.IntegerField(blank=True, null=True)
    is_random = models.BooleanField(blank=True, null=True)
    lane = models.IntegerField(blank=True, null=True)
    streak_prediction = models.IntegerField(blank=True, null=True)
    intentional_feeding = models.BooleanField(blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    imp = models.IntegerField(blank=True, null=True)
    award = models.IntegerField(blank=True, null=True)
    item0_id = models.IntegerField(blank=True, null=True)
    item1_id = models.IntegerField(blank=True, null=True)
    item2_id = models.IntegerField(blank=True, null=True)
    item3_id = models.IntegerField(blank=True, null=True)
    item4_id = models.IntegerField(blank=True, null=True)
    item5_id = models.IntegerField(blank=True, null=True)
    backpack0_id = models.IntegerField(blank=True, null=True)
    backpack1_id = models.IntegerField(blank=True, null=True)
    backpack2_id = models.IntegerField(blank=True, null=True)
    behavior = models.IntegerField(blank=True, null=True)
    hero_healing = models.IntegerField(blank=True, null=True)
    roam_lane = models.IntegerField(blank=True, null=True)
    abilities = models.JSONField(blank=True, null=True)
    is_victory = models.BooleanField(blank=True, null=True)
    networth = models.IntegerField(blank=True, null=True)
    neutral0_id = models.IntegerField(blank=True, null=True)
    additional_unit = models.ForeignKey(
        MatchPlayerAdditionalUnit, on_delete=models.CASCADE, blank=True, null=True
    )
    dota_plus_hero_xp = models.IntegerField(blank=True, null=True)
    invisible_seconds = models.IntegerField(blank=True, null=True)
    match_player_stats = models.JSONField(blank=True, null=True)

    stats = models.JSONField(blank=True, null=True)
    playback_data = models.JSONField(blank=True, null=True)

    steam_account = models.ForeignKey(
        SteamAccount, to_field='id', on_delete=models.CASCADE, blank=True, null=True
    )
    is_dire = models.BooleanField(blank=True, null=True)
    role_basic = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    base_slot = models.IntegerField(blank=True, null=True)
    kda = models.FloatField(blank=True, null=True)
    map_location_home_fountain = models.IntegerField(blank=True, null=True)
    faction = models.IntegerField(blank=True, null=True)
    calculate_imp_lane = models.IntegerField(blank=True, null=True)
    game_version_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f" player {self.steam_account_id}"


class CourierEvent(Event):
    id = models.IntegerField(blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True)
    is_radiant = models.BooleanField(blank=True, null=True)


class CourierEventDetail(Event):
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    hp = models.FloatField(blank=True, null=True)
    is_flying = models.BooleanField(blank=True, null=True)
    respawn_time = models.FloatField(blank=True, null=True)
    item0Id = models.IntegerField(blank=True, null=True)
    item1Id = models.IntegerField(blank=True, null=True)
    item2Id = models.IntegerField(blank=True, null=True)
    item3Id = models.IntegerField(blank=True, null=True)
    item4Id = models.IntegerField(blank=True, null=True)
    item5Id = models.IntegerField(blank=True, null=True)
    courier_event = models.ForeignKey(CourierEvent, related_name='events', on_delete=models.CASCADE, blank=True,
                                      null=True)


# Rune Event Model
class MatchRuneEvent(Event):
    id = models.IntegerField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    location = models.IntegerField(blank=True, null=True)
    rune_type = models.IntegerField(blank=True, null=True)
    action = models.IntegerField(blank=True, null=True)


# Ward Event Model
class WardEvent(Event):
    id = models.IntegerField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    ward_type = models.IntegerField(blank=True, null=True)
    action = models.IntegerField(blank=True, null=True)
    player_destroyed = models.IntegerField(blank=True, null=True)
    from_player = models.IntegerField(blank=True, null=True)


# Tower Death Event Model
class TowerDeathEvent(Event):
    radiant = models.IntegerField(blank=True, null=True)
    dire = models.IntegerField(blank=True, null=True)


# Roshan Event Model
class RoshanEvent(Event):
    hp = models.FloatField(blank=True, null=True)
    max_hp = models.FloatField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    item0 = models.IntegerField(blank=True, null=True)


# Building Event Model
class BuildingEvent(Event):
    id = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    hp = models.FloatField(blank=True, null=True)
    max_hp = models.FloatField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    is_radiant = models.BooleanField(blank=True, null=True)
    npc_id = models.IntegerField(blank=True, null=True)


# Match Playback Data Model
class MatchPlaybackData(BaseModel):
    courier_events = models.ManyToManyField(CourierEvent, related_name='match_playback_data')
    rune_events = models.ManyToManyField(MatchRuneEvent, related_name='match_playback_data')
    ward_events = models.ManyToManyField(WardEvent, related_name='match_playback_data')
    tower_death_events = models.ManyToManyField(TowerDeathEvent, related_name='match_playback_data')
    roshan_events = models.ManyToManyField(RoshanEvent, related_name='match_playback_data')
    building_events = models.ManyToManyField(BuildingEvent, related_name='match_playback_data')
    radiant_captain_hero_id = models.IntegerField(blank=True, null=True)
    dire_captain_hero_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f" radiant_captain_hero_id {self.radiant_captain_hero_id}"

    def delete(self, using=None, keep_parents=False):
        self.courier_events.all().delete()
        self.rune_events.all().delete()
        self.ward_events.all().delete()
        self.tower_death_events.all().delete()
        self.roshan_events.all().delete()
        self.building_events.all().delete()
        super(MatchPlaybackData, self).delete(using, keep_parents)

    def restore(self):
        self.deleted_at = None
        self.courier_events.update(deleted_at=None)
        self.rune_events.update(deleted_at=None)
        self.ward_events.update(deleted_at=None)
        self.tower_death_events.update(deleted_at=None)
        self.roshan_events.update(deleted_at=None)
        self.building_events.update(deleted_at=None)
        self.save()


class MatchManager(BaseManager):
    def path_7_36c(self):
        return self.get_queryset().filter(game_version_id=175)


class Match(BaseModel):
    id = models.PositiveBigIntegerField(unique=True)
    did_radiant_win = models.BooleanField(blank=True, null=True)
    duration_seconds = models.PositiveBigIntegerField(blank=True, null=True)
    start_date_time = models.BigIntegerField(blank=True, null=True)
    tower_status_radiant = models.PositiveBigIntegerField(blank=True, null=True)
    tower_status_dire = models.PositiveBigIntegerField(blank=True, null=True)
    barracks_status_radiant = models.PositiveBigIntegerField(blank=True, null=True)
    barracks_status_dire = models.PositiveBigIntegerField(blank=True, null=True)
    cluster_id = models.PositiveBigIntegerField(blank=True, null=True)
    first_blood_time = models.IntegerField(blank=True, null=True)
    lobby_type = models.PositiveBigIntegerField(blank=True, null=True)
    num_human_players = models.PositiveBigIntegerField(blank=True, null=True)
    game_mode = models.PositiveBigIntegerField(blank=True, null=True)
    replay_salt = models.PositiveBigIntegerField(blank=True, null=True)
    is_stats = models.BooleanField(blank=True, null=True)
    tournament_id = models.PositiveBigIntegerField(blank=True, null=True)
    tournament_round = models.PositiveBigIntegerField(blank=True, null=True)
    average_rank = models.PositiveBigIntegerField(blank=True, null=True)
    actual_rank = models.PositiveBigIntegerField(blank=True, null=True)
    average_imp = models.PositiveBigIntegerField(blank=True, null=True)
    parsed_date_time = models.PositiveBigIntegerField(blank=True, null=True)
    stats_date_time = models.PositiveBigIntegerField(blank=True, null=True)
    league = models.ForeignKey(
        League,
        to_field='id',
        related_name="matches",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    radiant_team = models.ForeignKey(
        Team,
        to_field='id',
        on_delete=models.SET_NULL,
        related_name="radiant_matches",
        blank=True,
        null=True,
    )
    dire_team = models.ForeignKey(
        Team,
        to_field='id',
        on_delete=models.SET_NULL,
        related_name="dire_matches",
        blank=True,
        null=True,
    )
    series = models.ForeignKey(
        Series,
        to_field='id',
        on_delete=models.SET_NULL,
        related_name="matches",
        blank=True,
        null=True
    )
    game_version_id = models.PositiveBigIntegerField(blank=True, null=True)
    region_id = models.PositiveBigIntegerField(blank=True, null=True)
    sequence_num = models.PositiveBigIntegerField(blank=True, null=True)
    rank = models.PositiveBigIntegerField(blank=True, null=True)
    bracket = models.PositiveBigIntegerField(blank=True, null=True)
    end_date_time = models.PositiveBigIntegerField(blank=True, null=True)
    actual_rank_weight = models.PositiveBigIntegerField(blank=True, null=True)
    playback_data = models.OneToOneField(
        MatchPlaybackData,
        on_delete=models.SET_NULL,
        related_name="match",
        blank=True,
        null=True,
    )
    pick_bans = models.ManyToManyField(MatchPickBan, blank=True)
    spectators = models.ManyToManyField(MatchPlayerSpectator, blank=True)
    players = models.ManyToManyField(MatchPlayer, blank=True)
    analysis_outcome = models.PositiveBigIntegerField(blank=True, null=True)
    predicted_outcome_weight = models.PositiveBigIntegerField(blank=True, null=True)
    bottom_lane_outcome = models.PositiveBigIntegerField(blank=True, null=True)
    mid_lane_outcome = models.PositiveBigIntegerField(blank=True, null=True)
    top_lane_outcome = models.PositiveBigIntegerField(blank=True, null=True)
    radiant_networth_lead = models.TextField(blank=True, null=True)
    radiant_experience_lead = models.TextField(blank=True, null=True)
    radiant_kills = models.TextField(blank=True, null=True)
    dire_kills = models.TextField(blank=True, null=True)
    tower_status = models.JSONField(blank=True, null=True)
    lane_report = models.JSONField(blank=True, null=True)
    win_rates = models.TextField(blank=True, null=True)
    predicted_win_rates = models.TextField(blank=True, null=True)
    tower_deaths = models.JSONField(blank=True, null=True)
    chat_events = models.JSONField(blank=True, null=True)
    did_request_download = models.BooleanField(blank=True, null=True)
    radiant_players = models.ManyToManyField(
        MatchPlayer, related_name="radiant_matches_played", blank=True
    )
    dire_players = models.ManyToManyField(
        MatchPlayer, related_name="dire_matches_played", blank=True
    )
    game_result = models.PositiveBigIntegerField(blank=True, null=True)

    objects = MatchManager()

    def __str__(self):
        return f" match {self.id}"

    class Meta:
        db_table = "matches"
        ordering = ["-start_date_time"]

    def get_absolute_url(self):
        return f"/matches/{self.id}/"

    def get_verbose_start_datetime(self) -> datetime:
        return unix_to_datetime(self.start_date_time, settings.TIME_ZONE)

    def get_verbose_duration_seconds(self) -> timedelta | int | None:
        return seconds_to_hours_minutes(self.duration_seconds)

    def get_count_dire_kills(self):
        return sum_elements(self.dire_kills)

    def get_count_radiant_kills(self):
        return sum_elements(self.radiant_kills)
