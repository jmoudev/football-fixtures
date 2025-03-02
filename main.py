from datetime import datetime

from requests_cache import CachedSession
import typer


def _get_teams(session):
    response = session.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    response.raise_for_status()
    teams = {team["name"]: team["id"] for team in response.json()["teams"]}
    return teams


def _get_fixtures(session):
    response = session.get("https://fantasy.premierleague.com/api/fixtures/")
    response.raise_for_status()
    fixtures = response.json()
    return fixtures


def _get_id_from_team(team, teams):
    return teams[team.capitalize()]


def _get_team_from_id(team_id, teams):
    return [item[0] for item in teams.items() if item[1] == team_id][0]


def _get_readable_datetime(timestamp):
    _datetime = datetime.fromisoformat(timestamp)
    return f"{_datetime.strftime('%d %b %H:%M')}"


def main(team: str):
    session = CachedSession(".fpl_cache", backend="sqlite")

    teams = _get_teams(session)
    team_id = _get_id_from_team(team, teams)

    fixtures = _get_fixtures(session)

    team_fixtures = [
        fixture
        for fixture in fixtures
        if fixture["team_h"] == team_id or fixture["team_a"] == team_id
    ]
    # recent_fixtures = [fixture for fixture in team_fixtures if fixture["finished"]][-5:]
    upcoming_fixtures = [
        fixture for fixture in team_fixtures if not fixture["finished"]
    ][:5]
    print("Upcoming Fixtures:")
    for fixture in upcoming_fixtures:
        fixture_string = f"- {_get_team_from_id(fixture['team_h'], teams)} vs {_get_team_from_id(fixture['team_a'], teams)}, {_get_readable_datetime(fixture['kickoff_time'])}"
        print(fixture_string)


if __name__ == "__main__":
    typer.run(main)
