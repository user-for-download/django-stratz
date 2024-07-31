import logging
from datetime import datetime

from django.conf import settings
from django.db import models

from dj.common.models import BaseModel, BaseManager
from dj.common.utils import unix_to_datetime, string_to_datetime
from dj.stats.models import PopularMatchPickBan
from dj.teams.models import Team

logger = logging.getLogger(__name__)


class ProSteamAccount(BaseModel):
    steam_account_id = models.PositiveBigIntegerField(unique=True, editable=False)
    name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    fantasy_role = models.IntegerField(blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    sponsor = models.CharField(max_length=100, blank=True, null=True)
    is_locked = models.BooleanField(default=False, null=True)
    is_pro = models.BooleanField(default=False, null=True)
    total_earnings = models.IntegerField(blank=True, null=True)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    romanized_real_name = models.CharField(max_length=100, blank=True, null=True)
    roles = models.IntegerField(blank=True, null=True)
    aliases = models.CharField(max_length=255, blank=True, null=True)
    statuses = models.IntegerField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    twitch_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    vk_link = models.URLField(blank=True, null=True)
    you_tube_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    weibo_link = models.URLField(blank=True, null=True)
    signature_heroes = models.CharField(max_length=255, blank=True, null=True)
    countries = models.CharField(max_length=255, blank=True, null=True)
    ti_wins = models.IntegerField(blank=True, null=True)
    is_ti_winner = models.BooleanField(default=False, null=True)
    position = models.IntegerField(blank=True, null=True)


class SteamAccountManager(BaseManager):
    def acc_is_pro(self):
        """
        Returns pro_steam_account
        """
        return self.active().filter(pro_steam_account__is_pro=True)


class SteamAccount(BaseModel):
    id = models.PositiveBigIntegerField(unique=True, editable=False)
    last_active_time = models.CharField(max_length=50, blank=True, null=True)
    profile_uri = models.URLField(blank=True, null=True)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    time_created = models.CharField(max_length=50, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    state_code = models.CharField(max_length=10, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    community_visible_state = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    last_log_off = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    primary_clan_id = models.PositiveBigIntegerField(blank=True, null=True)
    solo_rank = models.IntegerField(blank=True, null=True)
    party_rank = models.IntegerField(blank=True, null=True)
    is_dota_plus_subscriber = models.BooleanField(default=False, null=True)
    dota_plus_original_start_date = models.CharField(max_length=50, blank=True, null=True)
    is_anonymous = models.BooleanField(default=False, null=True)
    is_stratz_public = models.BooleanField(default=False, null=True)
    season_rank = models.IntegerField(blank=True, null=True)
    season_leaderboard_rank = models.IntegerField(blank=True, null=True)
    season_leaderboard_division_id = models.IntegerField(blank=True, null=True)
    pro_steam_account = models.ForeignKey(
        ProSteamAccount,
        to_field='steam_account_id',
        related_name='steam_account',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    smurf_flag = models.IntegerField(blank=True, null=True)
    smurf_check_date = models.CharField(max_length=50, blank=True, null=True)
    last_match_date_time = models.CharField(max_length=50, blank=True, null=True)
    last_match_region_id = models.IntegerField(blank=True, null=True)
    dota_account_level = models.IntegerField(blank=True, null=True)
    rank_shift = models.IntegerField(blank=True, null=True)
    bracket = models.IntegerField(blank=True, null=True)
    bracket_basic_ids = models.IntegerField(blank=True, null=True)

    objects = SteamAccountManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/players/{self.id}/"


class BattlePass(BaseModel):
    event_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=10, null=True)
    bracket = models.IntegerField(blank=True, null=True)
    is_anonymous = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.event_id}"


class PlayerName(BaseModel):
    name = models.CharField(max_length=100)
    last_seen_date_time = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} to {unix_to_datetime(self.last_seen_date_time, settings.TIME_ZONE)}"


class SeasonRank(BaseModel):
    season_rank_id = models.IntegerField(blank=True, null=True)
    as_of_date_time = models.CharField(max_length=50, blank=True, null=True)
    is_core = models.BooleanField(default=False, null=True)
    rank = models.IntegerField(blank=True, null=True)


class PlayerBadge(BaseModel):
    steam_id = models.BigIntegerField(blank=True, null=True)
    badge_id = models.IntegerField(blank=True, null=True)
    slot = models.IntegerField(blank=True, null=True)
    created_date_time = models.CharField(max_length=50, blank=True, null=True)


class PlayerManager(BaseManager):
    def pro_player(self):
        """
        Returns pro_steam_account
        """
        return self.active().filter(steam_account__pro_steam_account__is_pro=True)


class TeamMember(BaseModel):
    steam_account = models.ForeignKey(
        SteamAccount,
        to_field='id',
        related_name="team",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    team = models.ForeignKey(
        Team,
        to_field='id',
        related_name="members",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    first_match_id = models.PositiveBigIntegerField(blank=True, null=True)
    first_match_date_time = models.CharField(max_length=220, null=True, blank=True)
    last_match_id = models.PositiveBigIntegerField(blank=True, null=True)
    last_match_date_time = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return f"{self.team.id}"

    def get_verbose_last_match_date_time(self) -> datetime | None:
        return string_to_datetime(self.last_match_date_time)

    def get_verbose_first_match_date_time(self) -> datetime | None:
        return string_to_datetime(self.first_match_date_time)

    def get_url_first_match(self):
        return f"/matches/{self.first_match_id}/"

    def get_url_last_match(self):
        return f"/matches/{self.last_match_id}/"


class Player(BaseModel):
    id = models.PositiveBigIntegerField(unique=True, editable=False)
    steam_account = models.OneToOneField(
        SteamAccount,
        to_field='id',
        related_name="player",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    battle_pass = models.ManyToManyField(BattlePass, blank=True)
    last_match_date = models.CharField(max_length=50, blank=True, null=True)
    badges = models.ManyToManyField(PlayerBadge, blank=True)
    last_region_id = models.PositiveBigIntegerField(blank=True, null=True)
    ranks = models.ManyToManyField(SeasonRank, blank=True)
    language_codes = models.JSONField(blank=True, null=True)
    first_match_date = models.PositiveBigIntegerField(blank=True, null=True)
    match_count = models.PositiveBigIntegerField(blank=True, null=True)
    win_count = models.PositiveBigIntegerField(blank=True, null=True)
    names = models.ManyToManyField(PlayerName, blank=True)
    team = models.OneToOneField(TeamMember, on_delete=models.CASCADE, blank=True, null=True)
    behavior_score = models.IntegerField(blank=True, null=True)
    is_followed = models.BooleanField(default=False, null=True)
    is_favorite = models.BooleanField(default=False, null=True)
    pick_bans = models.ManyToManyField(PopularMatchPickBan, related_name="player", blank=True)
    objects = PlayerManager()

    def __str__(self):
        return f"{self.id}"

    def get_real_name(self):
        return f"{self.steam_account.pro_steam_account.real_name}"

    def get_badges(self):
        return self.badges.filter(deleted_at__isnull=True)

    def get_battle_pass(self):
        return self.battle_pass.filter(deleted_at__isnull=True)

    def get_ranks(self):
        return self.ranks.filter(deleted_at__isnull=True)

    def get_names(self):
        return self.names.filter(deleted_at__isnull=True)

    def get_verbose_first_match_date(self) -> datetime | None:
        return unix_to_datetime(self.first_match_date)

    def get_absolute_url(self):
        return f"/players/{self.id}/"
