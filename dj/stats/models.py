from django.db import models

from dj.common.constants import TASK_TYPE_CHOICES
from dj.common.models import BaseModel


class PopularMatchPickBan(BaseModel):
    time_stamp_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    hero_picks = models.JSONField(blank=True, null=True)
    hero_bans = models.JSONField(blank=True, null=True)
    entity_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES, default='all')
    entity_id = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_entity_type_display()} {self.entity_id}"
