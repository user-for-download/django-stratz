import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, Union, Callable

import pytz
import requests
from django.conf import settings
from django.db.models import Model
from django.db.models.query import QuerySet
from jsonschema import validate, exceptions
from orjson import orjson

from dj.common.constants import HEROES

logger = logging.getLogger(__name__)

URL_IMG_HERO = 'https://dj.binetc.site/static/images/heroes'


def now_tz(tz: str = settings.TIME_ZONE) -> datetime:
    return datetime.now(pytz.timezone(tz))


def datetime_to_int(dt: datetime = datetime.now(pytz.timezone(settings.TIME_ZONE))) -> int:
    """
    Convert a datetime object to a Unix timestamp (integer representation).

    Args:
        dt (datetime): The datetime object to convert.

    Returns:
        int: The Unix timestamp representing the datetime object.
    """
    try:
        return int(dt.timestamp())
    except Exception as e:
        logger.error(f"Exception in datetime_to_int: {repr(e)}")
        return 0


def validate_json(json_data: Any, schema: Dict[str, Any]) -> bool:
    """
    Validates JSON data against the given schema.

    Args:
        json_data (Any): The JSON data to validate.
        schema (Dict[str, Any]): The schema to validate against.

    Returns:
        bool: True if validation is successful, False otherwise.
    """
    try:
        validate(instance=json_data, schema=schema)
        return True
    except exceptions.ValidationError as err:
        logger.error(f"JSON validation error: {repr(err)}")
        return False


def response_to_json(url: str, schema: Dict[str, Any]) -> Optional[Any]:
    """
    Makes a GET request to the specified URL, validates the response JSON
    against the given schema, and returns the JSON data if valid.

    Args:
        url (str): The URL to make the GET request to.
        schema (Dict[str, Any]): The schema to validate the response JSON against.

    Returns:
        Optional[Any]: The validated JSON data or None if an error occurs.
    """
    try:
        token = settings.TOKEN_STRATZ
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if validate_json(json_data, schema):
            return json_data
        else:
            logger.warning(f"JSON validation failed for URL: {url}")
            return None
    except requests.exceptions.SSLError as e:
        logger.error(f"SSL error occurred: {e}")
    except requests.RequestException as e:
        logger.error(f"RequestException while requesting URL {url}: {repr(e)}")
    except ValueError as e:
        logger.error(f"ValueError while parsing JSON from URL {url}: {repr(e)}")
    except Exception as e:
        logger.error(f"Unexpected exception: {repr(e)}")
    return None


def iso8601_to_int(date_string: Union[str, None]) -> Union[int, str]:
    """
    Convert an ISO 8601 date string to a Unix timestamp.

    Args:
        date_string (str): The ISO 8601 formatted date string.

    Returns:
        Union[int, str]: The Unix timestamp if conversion is successful,
                         otherwise the original date string.
    """
    try:
        date_string = date_string if isinstance(date_string, str) else "1990-01-21T00:01:01"
        date_obj = datetime.fromisoformat(date_string)
        timestamp = int(date_obj.timestamp())
        return timestamp
    except ValueError:
        logger.error("Invalid date format")
        return date_string


def seconds_to_hours_minutes(duration_seconds: Union[int, None]) -> Union[timedelta, int, None]:
    """
    Convert duration in seconds to a timedelta object.

    Args:
        duration_seconds (int): The duration in seconds.

    Returns:
        Union[timedelta, int, None]: The duration as a timedelta object if conversion is successful,
                                     otherwise the original duration.
    """
    try:
        duration_seconds = duration_seconds if isinstance(duration_seconds, int) else 0
        duration_timedelta = timedelta(seconds=duration_seconds)
        return duration_timedelta
    except Exception as e:
        logger.error(f"seconds_to_hours_minutes exception: {repr(e)}")
        return duration_seconds


def unix_to_datetime(unix_timestamp: Optional[int], tz: str = settings.TIME_ZONE) -> Optional[datetime]:
    """
    Convert a Unix timestamp to a timezone-aware datetime object.

    Args:
        unix_timestamp (int): Unix timestamp.
        tz (str, optional): Timezone string (e.g., 'America/New_York'). Defaults to None.

    Returns:
        Optional[datetime]: Timezone-aware datetime object, or None if conversion fails.
    """
    try:
        cur_tz = pytz.timezone(tz)
        return datetime.fromtimestamp(unix_timestamp, cur_tz)
    except Exception as e:
        logger.error(f"unix_to_datetime exception: {repr(e)}")
    return None


def string_to_datetime(date_string: Optional[str], tz_string: str = settings.TIME_ZONE) -> Optional[datetime]:
    try:
        if date_string:
            naive_dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
            timezone_py = pytz.timezone(tz_string)
            aware_dt = timezone_py.localize(naive_dt)
            return aware_dt
    except ValueError as e:
        logger.error(f"Invalid date string format: {date_string}: {repr(e)}")
    except pytz.UnknownTimeZoneError as e:
        logger.error(f"Unknown timezone: {repr(e)}")
    return None


def process_entities(entity_queryset: QuerySet, task_function: Callable[[int], Any], entity_name: str) -> None:
    """
    Universal function to process pro entities.

    Args:
        entity_queryset (QuerySet): Queryset to retrieve entity IDs.
        task_function (Callable[[int], Any]): The task function to be called (e.g., task_get_and_save_player).
        entity_name (str): String representing the entity type (e.g., 'Player' or 'Account').
    """
    try:
        entity_ids = list(entity_queryset.values_list("id", flat=True))
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(task_function, entity_id): entity_id for entity_id in entity_ids}
            for future in futures:
                entity_id = futures[future]
                try:
                    future.result()  # Wait for all tasks to complete
                    logger.info("%s ID: %s", entity_name, entity_id)
                except Exception as e:
                    logger.error("Error processing %s ID: %s, error: %s", entity_name, entity_id, repr(e))
    except Exception as e:
        logger.error("Failed to process %s entities: %s", entity_name, repr(e))


def process_entities_1(entity_queryset: QuerySet, task_function: Callable[[int], Any], entity_name: str) -> None:
    """
    Universal function to process pro entities.

    Args:
        entity_queryset (QuerySet): Queryset to retrieve entity IDs.
        task_function (Callable[[int], Any]): The task function to be called (e.g., task_get_and_save_player).
        entity_name (str): String representing the entity type (e.g., 'Player' or 'Account').
    """
    try:
        entity_ids = entity_queryset.values_list("id", flat=True)
        for entity_id in entity_ids:
            task_function(entity_id)
            logger.info("%s ID: %s", entity_name, entity_id)
    except Exception as e:
        logger.error(f"Failed to process {entity_name} entities: {repr(e)}")


def save_data_if_exists(
    data: Optional[Dict[str, Any]],
    key: str,
    func: Callable[[Dict[str, Any]], Optional[Model]]
) -> Optional[Model]:
    if isinstance(data, dict) and key in data:
        save_data = data.get(key)
        if save_data is not None and callable(func):
            try:
                return func(save_data)
            except TypeError as e:
                logger.error("Error in save_data_if_exists with function %s: %s", func, e)
    return None


def process_related_data_1(
    data: Optional[Dict[str, Any]],
    key: str,
    save_function: Callable[..., Any],
    *args: Any
) -> None:
    try:
        if data and key in data:
            items = data.get(key, [])
            items = items if isinstance(items, list) else [items]
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(save_function, item, *args) for item in items]
                for future in futures:
                    future.result()  # Wait for all tasks to complete
    except Exception as e:
        logger.error(f"process_related_data: Error processing related data for key '{key}': {e}")


def process_related_data(
    data: Optional[Dict[str, Any]],
    key: str,
    save_function: Callable[..., Any],
    *args: Any
) -> None:
    try:
        if data and key in data:
            items = data.get(key, [])
            items = items if isinstance(items, list) else [items]
            for item in items:
                save_function(item, *args)
    except Exception as e:
        logger.error(f"process_related_data: Error processing related data for key '{key}': {e}")


def get_hero_info(hero_id: int) -> tuple:
    try:
        hero_info = HEROES.get(hero_id, "default.png")  # Replace "default" with your desired default value
        hero_name = hero_info.split(".")[0]
        hero_image_url = f"{URL_IMG_HERO}/npc_dota_hero_{hero_info}"
        return hero_name, hero_image_url
    except Exception as e:
        logger.error(f"get_hero_info An unexpected error occurred: {str(e)}")


def scale_size(count, min_count, max_count, min_size=30, max_size=100):
    if max_count == min_count:
        return (max_size + min_size) / 2
    return min_size + (count - min_count) * (max_size - min_size) / (max_count - min_count)


def sum_elements(input_string: str) -> Union[int, str]:
    try:
        # Convert the input string to a list of integers
        input_list = eval(input_string)

        # Ensure the result is a list
        if not isinstance(input_list, list):
            logger.error(ValueError("Input string does not evaluate to a list."))

        # Calculate the sum of the elements in the list
        total_sum = sum(input_list)

        return total_sum
    except Exception as e:
        logger.error(f"sum_elements An unexpected error occurred: {str(e)}")


def get_delta_time(last_dt: datetime, tz: str = settings.TIME_ZONE) -> str:
    try:
        now = datetime.now(pytz.timezone(tz))
        delta = now - last_dt
        if delta.days > 1:
            return last_dt.strftime('%d.%m.%Y')
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if hours > 1:
            return f"{hours}h:{minutes}m ago"
        return f"{minutes}m ago"
    except Exception as e:
        logger.error(f"get_hero_info An unexpected error occurred: {str(e)}")
        return f"ERh:ERm ago"


def load_json(file_name: str = '') -> dict:
    try:
        with open(file_name, 'rb') as file:
            data = orjson.loads(file.read())
        return data
    except Exception as e:
        logger.error(f"load_json An unexpected error occurred: {str(e)}")


def to_abs(my_dict: Dict[str, Any], key: str) -> Union[int, None]:
    try:
        if my_dict and key in my_dict:
            value = my_dict[key]
            if isinstance(value, int):
                return abs(value)

        return None
    except Exception as e:
        logger.error(f"to_abs An unexpected error occurred: {str(e)}")
        return None
