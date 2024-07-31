# Create your models here.
from django.db import models

from dj.common.models import BaseModel


class Ability(BaseModel):
    slot = models.IntegerField(blank=True, null=True)
    ability_id = models.IntegerField(blank=True, null=True)


class Role(BaseModel):
    role_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)


class Talent(BaseModel):
    slot = models.IntegerField(blank=True, null=True)
    game_version_id = models.IntegerField(blank=True, null=True)
    ability_id = models.IntegerField(blank=True, null=True)


class Stat(BaseModel):
    game_version_id = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)
    hero_unlock_order = models.IntegerField(blank=True, null=True)
    team = models.BooleanField(blank=True, null=True)
    cm_enabled = models.BooleanField(blank=True, null=True)
    new_player_enabled = models.BooleanField(blank=True, null=True)
    attack_type = models.CharField(max_length=255, blank=True, null=True)
    starting_armor = models.FloatField(blank=True, null=True)
    starting_magic_armor = models.FloatField(blank=True, null=True)
    starting_damage_min = models.FloatField(blank=True, null=True)
    starting_damage_max = models.FloatField(blank=True, null=True)
    attack_rate = models.FloatField(blank=True, null=True)
    attack_animation_point = models.FloatField(blank=True, null=True)
    attack_acquisition_range = models.FloatField(blank=True, null=True)
    attack_range = models.FloatField(blank=True, null=True)
    attribute_primary = models.CharField(max_length=255, blank=True, null=True)
    hero_primary_attribute = models.IntegerField(blank=True, null=True)
    strength_base = models.FloatField(blank=True, null=True)
    strength_gain = models.FloatField(blank=True, null=True)
    intelligence_base = models.FloatField(blank=True, null=True)
    intelligence_gain = models.FloatField(blank=True, null=True)
    agility_base = models.FloatField(blank=True, null=True)
    agility_gain = models.FloatField(blank=True, null=True)
    hp_regen = models.FloatField(blank=True, null=True)
    mp_regen = models.FloatField(blank=True, null=True)
    move_speed = models.FloatField(blank=True, null=True)
    move_turn_rate = models.FloatField(blank=True, null=True)
    hp_bar_offset = models.FloatField(blank=True, null=True)
    vision_daytime_range = models.FloatField(blank=True, null=True)
    vision_nighttime_range = models.FloatField(blank=True, null=True)
    complexity = models.IntegerField(blank=True, null=True)
    primary_attribute_enum = models.IntegerField(blank=True, null=True)


class Language(BaseModel):
    hero_id = models.IntegerField(blank=True, null=True)
    game_version_id = models.IntegerField(blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True, unique=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    hype = models.TextField(blank=True, null=True)


class Hero(BaseModel):
    id = models.PositiveSmallIntegerField(unique=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    abilities = models.ManyToManyField(Ability, blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    talents = models.ManyToManyField(Talent, blank=True)
    stat = models.OneToOneField(Stat, on_delete=models.CASCADE, blank=True, null=True)
    language = models.OneToOneField(Language, to_field='language_id', on_delete=models.CASCADE, blank=True, null=True)
    aliases = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return f"/heroes/{self.id}/"
