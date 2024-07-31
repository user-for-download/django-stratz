from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models

from dj.common.constants import LEAGUE_TIER_THRESHOLD, LEAGUE_ID_THRESHOLD
from dj.common.models import BaseModel, BaseManager
from dj.common.utils import datetime_to_int, get_delta_time, now_tz
from dj.common.utils import unix_to_datetime
from dj.stats.models import PopularMatchPickBan
from dj.teams.models import Team


class LeagueManager(BaseManager):
    def tier2(self):
        return self.active().filter(
            tier__gte=LEAGUE_TIER_THRESHOLD
        ).filter(
            id__gte=LEAGUE_ID_THRESHOLD
        ).filter(
            is_over=False
        ).order_by("-id")

    def need_to_update(self):
        return self.active().filter(tier__gte=2).filter(is_over=False)

    def update_is_over(self):
        self.active().filter(end_datetime__lt=datetime_to_int(), is_over=False).update(
            is_over=True
        )


class League(BaseModel):
    id = models.PositiveBigIntegerField(unique=True, editable=False)
    registration_period = models.PositiveSmallIntegerField(blank=True, null=True)
    country = models.CharField(max_length=220, null=True, blank=True)
    venue = models.CharField(max_length=220, null=True, blank=True)
    private = models.BooleanField(default=False, blank=True, null=True)
    city = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    has_live_matches = models.BooleanField(default=False, blank=True, null=True)
    tier = models.PositiveSmallIntegerField(blank=True, null=True)
    tournament_url = models.TextField(null=True, blank=True)
    free_to_spectate = models.BooleanField(default=False, blank=True, null=True)
    is_followed = models.BooleanField(default=False, blank=True, null=True)
    last_match_date = models.PositiveBigIntegerField(null=True, blank=True)
    pro_circuit_points = models.CharField(max_length=220, null=True, blank=True)
    banner = models.CharField(max_length=220, null=True, blank=True)
    stop_sales_time = models.CharField(max_length=15, null=True, blank=True)
    image_uri = models.TextField(null=True, blank=True)
    display_name = models.CharField(max_length=220, null=True, blank=True)
    end_datetime = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=220, null=True, blank=True)
    prize_pool = models.CharField(max_length=220, null=True, blank=True)
    base_prize_pool = models.CharField(max_length=220, null=True, blank=True)
    region = models.PositiveSmallIntegerField(blank=True, null=True)
    start_datetime = models.PositiveBigIntegerField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(blank=True, null=True)
    is_over = models.BooleanField(default=False, blank=True, null=True)
    pick_bans = models.ManyToManyField(PopularMatchPickBan, related_name="league", blank=True)

    objects = LeagueManager()

    def __str__(self):
        return self.display_name

    def delete(self, using=None, keep_parents=False):
        self.series.all().delete()
        super(League, self).delete(using, keep_parents)

    def restore(self):
        self.series.update(deleted_at=None)
        self.deleted_at = None
        self.save()

    class Meta:
        db_table = "leagues"
        ordering = ["-start_datetime"]

    def clean(self):
        if (
            self.start_datetime
            and self.end_datetime
            and self.start_datetime >= self.end_datetime
        ):
            raise ValidationError("End date cannot be before start date")

    def get_absolute_url(self):
        return f"/leagues/{self.id}/"

    def get_verbose_start_datetime(self) -> datetime:
        return unix_to_datetime(self.start_datetime)

    def get_verbose_end_datetime(self) -> datetime:
        return unix_to_datetime(self.end_datetime)

    @property
    def has_started(self) -> bool:
        return self.start_datetime >= datetime_to_int()


class SeriesManager(BaseManager):
    def need_to_update(self):
        return self.active().filter(is_over=False)

    def update_is_over(self):
        self.active().filter(
            last_match_date_time__lt=datetime_to_int(now_tz() - timedelta(hours=12)),
            is_over=False,
        ).update(is_over=True)


class Series(BaseModel):
    id = models.PositiveBigIntegerField(unique=True, editable=False)
    type = models.PositiveSmallIntegerField(blank=True, null=True)
    team_one = models.ForeignKey(
        Team,
        to_field='id',
        on_delete=models.CASCADE,
        related_name="teams_one_series",
        blank=True,
        null=True,
    )
    team_two = models.ForeignKey(
        Team,
        to_field='id',
        on_delete=models.CASCADE,
        related_name="teams_two_series",
        blank=True,
        null=True,
    )
    league = models.ForeignKey(
        League, to_field='id', on_delete=models.CASCADE, related_name="series", blank=True, null=True
    )
    team_one_win_count = models.PositiveSmallIntegerField(blank=True, null=True)
    team_two_win_count = models.PositiveSmallIntegerField(blank=True, null=True)
    winning_team_id = models.PositiveIntegerField(blank=True, null=True)
    last_match_date_time = models.PositiveBigIntegerField(blank=True, null=True)
    losing_team_id = models.PositiveIntegerField(blank=True, null=True)
    is_over = models.BooleanField(default=False, blank=True, null=True)

    objects = SeriesManager()

    def __str__(self):
        return f"{self.id}-lg{self.league_id}-win-{self.winning_team_id}"

    class Meta:
        db_table = "series"
        ordering = ["-last_match_date_time"]

    def get_absolute_url(self):
        return f"/leagues/{self.league_id}/series/{self.id}/"

    @property
    def get_verbose_updated_at(self):
        return datetime_to_int(self.updated_at)

    @property
    def get_verbose_last_match_date_time(self):
        last_match_dt = unix_to_datetime(self.last_match_date_time)
        return get_delta_time(last_match_dt)

    @property
    def get_bo_format_name(self):
        match self.type:
            case 1:
                bo = 3
            case 2:
                bo = 5
            case 3:
                bo = 2
            case _:
                bo = 1
        return bo

    @property
    def get_title_team_one(self):
        team_one_name = self.team_one.name if self.team_one and self.team_one.name else f"Team {self.team_one.id}"
        if self.winning_team_id == self.team_one.id:
            return f'<span class="badge text-bg-success">{team_one_name}</span>'
        return team_one_name

    @property
    def get_title_team_two(self):
        team_two_name = self.team_two.name if self.team_two and self.team_two.name else f"Team {self.team_two.id}"
        if self.winning_team_id == self.team_two.id:
            return f'<span class="badge text-bg-success">{team_two_name}</span>'
        return team_two_name

    @property
    def get_matches(self):
        return self.matches.active()
