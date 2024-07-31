import json


def create_cut_heroes(input_file, output_file):
    with open(input_file, 'r') as f:
        heroes = json.load(f)

    cut_heroes = {}
    for key, hero in heroes.items():
        cut_heroes[key] = {
            "id": hero["id"],
            "name": hero["name"],
            "img": hero["img"],
            "icon": hero["icon"]
        }

    with open(output_file, 'w') as f:
        json.dump(cut_heroes, f, indent=4)


# Usage
input_file = 'heroes.json'
output_file = 'cut_heroes.json'
create_cut_heroes(input_file, output_file)

import requests
import os
from typing import Optional, Any, Dict, Union, Callable
import json

def load_heroes_data(file_path: str = 'dj/common/json/heroes_cut.json') -> Dict[str, Any]:
    """
    Load heroes data from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing heroes data.

    Returns:
        Dict[str, Any]: A dictionary containing heroes data.

    Raises:
        FileNotFoundError: If the JSON file is not found.
        json.JSONDecodeError: If there is an error in decoding the JSON.
    """
    try:
        with open(file_path, 'r') as f:
            heroes_data = json.load(f)
            if not isinstance(heroes_data, dict):
                raise ValueError("The JSON file does not contain a valid dictionary.")
            return heroes_data
    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the file {file_path}.")
    except ValueError as ve:
        logger.error(f"ValueError from the file {ve}.")

url_image = "https://cdn.cloudflare.steamstatic.com"
output_folder = "dj/static/images/heroes/"
heroes = load_heroes_data()
# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate over heroes and download images
for hero_id, hero_data in heroes.items():
    hero_image_url = url_image + hero_data["img"]
    output_path = os.path.join(output_folder, f"{hero_data['name']}.png")
    response = requests.get(hero_image_url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded image for {hero_data['name']} to {output_path}")



def get_league_data(request, league_id):
    try:
        series = Series.objects.filter(id=league_id).first()
        league = League.objects.get(series=series)
        team_data = {
            'id': league.id,
            'name': league.display_name,
        }
        response_data = orjson.dumps(team_data)
        return HttpResponse(response_data, content_type='application/json')
    except League.DoesNotExist:
        response_data = orjson.dumps({'error': 'Team not found'})
        return HttpResponse(response_data, content_type='application/json', status=404)
