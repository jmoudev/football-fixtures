from datetime import datetime

import requests
from requests_cache import CachedSession

TEAM_IDS = {
    "Arsenal": 1,
    "Aston Villa": 2,
    "Bournemouth": 3,
    "Brentford": 4,
    "Brighton": 5,
    "Chelsea": 6,
    "Crystal Palace": 7,
    "Everton": 8,
    "Fulham": 9,
    "Ipswich": 10,
    "Leicester": 11,
    "Liverpool": 12,
    "Man City": 13,
    "Man Utd": 14,
    "Newcastle": 15,
    "Nott'm Forest": 16,
    "Southampton": 17,
    "Spurs": 18,
    "West Ham": 19,
    "Wolves": 20,
}


def _get_id_from_team(team):
    return TEAM_IDS[team]


def _get_team_from_id(team_id):
    return [item[0] for item in TEAM_IDS.items() if item[1] == team_id][0]


def _get_readable_datetime(timestamp):
    _datetime = datetime.fromisoformat(timestamp)
    return f"{_datetime.strftime("%d %b %H:%M")}"


def main():
    session = CachedSession('.fixture_cache', backend='sqlite')

    team = "Newcastle"
    team_id = _get_id_from_team(team)

    try:
        response = session.get("https://fantasy.premierleague.com/api/fixtures/")
        response.raise_for_status()
        # TODO: handle json decode error
        fixtures = response.json()
    except requests.HTTPError as http_error:
        raise http_error

    team_fixtures = [fixture for fixture in fixtures if fixture["team_h"] == team_id or fixture["team_a"] == team_id]
    recent_fixtures = [fixture for fixture in team_fixtures if fixture["finished"] == True][-5:]
    upcoming_fixtures = [fixture for fixture in team_fixtures if fixture["finished"] == False][:5]
    print("Upcoming Fixtures:")
    for fixture in upcoming_fixtures:
        fixture_string = f"- {_get_team_from_id(fixture["team_h"])} vs {_get_team_from_id(fixture["team_a"])}, {_get_readable_datetime(fixture["kickoff_time"])}"
        print(fixture_string)


if __name__ == "__main__":
    main()
