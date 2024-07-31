import logging
from typing import Optional, Any, Dict

from django.core.exceptions import ValidationError
from django.db import transaction

from dj.common.urls import get_url_heroes
from dj.common.utils import save_data_if_exists, process_related_data, response_to_json
from dj.heroes.models import Stat, Language
from .models import Hero

logger = logging.getLogger(__name__)


def fetch_and_process_heroes() -> None:
    try:
        url = get_url_heroes()
        response = response_to_json(url, {})
        heroes = response if isinstance(response, dict) else {}
        for hero_id, hero_data in heroes.items():
            try:
                save_hero(hero_data)
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
            except Exception as e:
                logger.exception(f"An error occurred: {e}")
    except Exception as e:
        logger.error(
            f"fetch_and_process_heroes: An error occurred during the transaction: {e}"
        )


@transaction.atomic
def save_hero(hero_data: Dict[str, Any]) -> Optional[Hero]:
    try:
        stat = save_data_if_exists(hero_data, "stat", save_stats)
        language = save_data_if_exists(hero_data, "language", save_language)

        hero, _ = Hero.objects.update_or_create(
            id=hero_data.get("id"),
            defaults={
                "name": hero_data.get("name"),
                "display_name": hero_data.get("displayName"),
                "short_name": hero_data.get("shortName"),
                "stat": stat,
                "language": language,
                "aliases": hero_data.get("aliases", []),
            },
        )

        process_related_data(hero_data, "abilities", save_ability, hero)
        process_related_data(hero_data, "roles", save_role, hero)
        process_related_data(hero_data, "talents", save_talent, hero)

        return hero
    except Exception as e:
        logger.error("Failed to save hero: %s", e)
        return None


def save_ability(ability_data: Dict[str, Any], hero: Hero):
    try:
        hero.abilities.update_or_create(
            slot=ability_data.get("slot"), ability_id=ability_data.get("abilityId")
        )
    except Exception as e:
        logger.error("Failed to save hero ability: %s", e)
        return None


def save_role(role_data: Dict[str, Any], hero: Hero):
    try:
        hero.roles.update_or_create(
            role_id=role_data.get("roleId"), defaults={"level": role_data.get("level")}
        )
    except Exception as e:
        logger.error("Failed to save hero role: %s", e)
        return None


def save_talent(talent_data: Dict[str, Any], hero: Hero):
    try:
        hero.talents.update_or_create(
            slot=talent_data.get("slot"),
            game_version_id=talent_data.get("gameVersionId"),
            defaults={"ability_id": talent_data.get("abilityId")},
        )
    except Exception as e:
        logger.error("Failed to save hero talent: %s", e)
        return None


def save_stats(stat_data: Dict[str, Any]) -> Optional[Stat]:
    try:
        stat, _ = Stat.objects.update_or_create(
            game_version_id=stat_data.get("gameVersionId"),
            defaults={
                "enabled": stat_data.get("enabled"),
                "hero_unlock_order": stat_data.get("heroUnlockOrder"),
                "team": stat_data.get("team"),
                "cm_enabled": stat_data.get("cmEnabled"),
                "new_player_enabled": stat_data.get("newPlayerEnabled"),
                "attack_type": stat_data.get("attackType"),
                "starting_armor": stat_data.get("startingArmor"),
                "starting_magic_armor": stat_data.get("startingMagicArmor"),
                "starting_damage_min": stat_data.get("startingDamageMin"),
                "starting_damage_max": stat_data.get("startingDamageMax"),
                "attack_rate": stat_data.get("attackRate"),
                "attack_animation_point": stat_data.get("attackAnimationPoint"),
                "attack_acquisition_range": stat_data.get("attackAcquisitionRange"),
                "attack_range": stat_data.get("attackRange"),
                "attribute_primary": stat_data.get("AttributePrimary"),
                "hero_primary_attribute": stat_data.get("heroPrimaryAttribute"),
                "strength_base": stat_data.get("strengthBase"),
                "strength_gain": stat_data.get("strengthGain"),
                "intelligence_base": stat_data.get("intelligenceBase"),
                "intelligence_gain": stat_data.get("intelligenceGain"),
                "agility_base": stat_data.get("agilityBase"),
                "agility_gain": stat_data.get("agilityGain"),
                "hp_regen": stat_data.get("hpRegen"),
                "mp_regen": stat_data.get("mpRegen"),
                "move_speed": stat_data.get("moveSpeed"),
                "move_turn_rate": stat_data.get("moveTurnRate"),
                "hp_bar_offset": stat_data.get("hpBarOffset"),
                "vision_daytime_range": stat_data.get("visionDaytimeRange"),
                "vision_nighttime_range": stat_data.get("visionNighttimeRange"),
                "complexity": stat_data.get("complexity"),
                "primary_attribute_enum": stat_data.get("primaryAttributeEnum"),
            },
        )
    except Exception as e:
        logger.error("Failed to save hero stats: %s", e)
        return None


def save_language(language_data: Dict[str, Any]) -> Optional[Language]:
    try:
        # Save Language
        language, _ = Language.objects.update_or_create(
            game_version_id=language_data.get("gameVersionId"),
            defaults={
                "language_id": language_data.get("languageId"),
                "hero_id": language_data.get("heroId"),
                "display_name": language_data.get("displayName"),
                "bio": language_data.get("bio"),
                "hype": language_data.get("hype"),
            },
        )
    except Exception as e:
        logger.error("Failed to save hero language: %s", e)
        return None
