from datetime import datetime

from django.conf import settings
from django.db import models

from dj.common.models import BaseManager, BaseModel
from dj.common.utils import unix_to_datetime
from dj.stats.models import PopularMatchPickBan


class TeamManager(BaseManager):
    def is_pro(self):
        """
        Returns pro teams
        """
        return self.active().filter(rank__gte=1200).filter(is_pro=True).order_by('-rank')


class Team(BaseModel):
    id = models.PositiveBigIntegerField(unique=True, editable=False)
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.CharField(max_length=20, blank=True, null=True)
    is_pro = models.BooleanField(default=False, null=True)
    is_locked = models.BooleanField(default=False, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    base_logo = models.URLField(blank=True, null=True)
    banner_logo = models.URLField(blank=True, null=True)
    sponsor_logo = models.URLField(blank=True, null=True)
    win_count = models.IntegerField(blank=True, null=True)
    loss_count = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    last_match_date_time = models.BigIntegerField(blank=True, null=True)
    coach_steam_account_id = models.PositiveBigIntegerField(blank=True, null=True)
    is_followed = models.BooleanField(default=False, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    pick_bans = models.ManyToManyField(PopularMatchPickBan, related_name="team", blank=True)
    objects = TeamManager()

    class Meta:
        db_table = 'teams'
        ordering = ['-rank']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/teams/{self.id}/"

    def get_verbose_last_match_date_time(self) -> datetime | None:
        return unix_to_datetime(self.last_match_date_time, settings.TIME_ZONE)

    def get_members(self):
        return self.members.active().order_by('-last_match_id')
