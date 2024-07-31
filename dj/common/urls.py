API = 'https://api.stratz.com/api/v1'
URL_LAST_100_LEAGUES = f'{API}/league?take=100&orderBy=-startDateTime'
OPENDOTA_API = 'https://api.opendota.com/api'


def get_url_league_list(take: int = 250, order_by: str = '-id') -> str:
    return f'{API}/league?take={take}&orderBy={order_by}'


def get_url_league_match_list(league_id: int, take: int = 500, skip: int = 0) -> str:
    return f'{API}/league/{league_id}/matches?take={take}&skip={skip}'


def get_url_league_series_list(league_id: int, take: int = 500, skip: int = 0) -> str:
    return f'{API}/league/{league_id}/series?take={take}&skip={skip}'


def get_url_team(team_id: int = 0) -> str:
    return f'{API}/team/{team_id}'


def get_url_match(match_id: int = 0) -> str:
    return f'{API}/match/{match_id}'


def get_url_pro_steam_acc() -> str:
    return f'{API}/player/proSteamAccount'


def get_url_player(player_id: int = 0) -> str:
    return f'{API}/player/{player_id}'


def get_url_heroes() -> str:
    return f'{API}/Hero'


def get_opendota_teams() -> str:
    return f'{OPENDOTA_API}/explorer?sql=SELECT%20teams.*%2C%20team_rating.*%2C%0ASTRING_AGG(distinct(team_match.match_id%3A%3Acharacter%20varying)%2C%20%27%2C%20%27)%20as%20matches_ids%0AFROM%20teams%20%0ALEFT%20JOIN%20team_rating%20ON%20team_rating.team_id%20%3D%20teams.team_id%20%0ALEFT%20JOIN%20team_match%20ON%20team_match.team_id%20%3D%20teams.team_id%0ALEFT%20JOIN%20match_patch%20ON%20match_patch.match_id%20%3D%20team_match.match_id%0AWHERE%20team_rating.rating%20%3E%3D%201100%20AND%20match_patch.patch%20%3E%3D%20%277.33%27%0AGROUP%20BY%20teams.team_id%2C%20team_rating.team_id%0AORDER%20BY%20team_rating.rating%20DESC%0A%0A'
