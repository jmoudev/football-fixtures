from datetime import datetime
from typing_extensions import Annotated

from requests_cache import CachedSession
import typer


class InvalidTeamError(Exception):
    pass


class NoFixturesError(Exception):
    pass


FPL_BASE_URL = "https://fantasy.premierleague.com/api/"
TEAMS_URL = f"{FPL_BASE_URL}/bootstrap-static/"
FIXTURES_URL = f"{FPL_BASE_URL}/fixtures/"


app = typer.Typer(add_completion=False)


def _get_teams(session):
    response = session.get(TEAMS_URL)
    response.raise_for_status()
    teams = {team["name"]: team["id"] for team in response.json()["teams"]}
    return teams


def _get_fixtures(session):
    response = session.get(FIXTURES_URL)
    response.raise_for_status()
    fixtures = response.json()
    return fixtures


def _get_id_from_team(team, teams):
    try:
        return teams[team.capitalize()]
    except KeyError as e:
        raise InvalidTeamError(f"Invalid team: {team}") from e


def _get_team_from_id(team_id, teams):
    return [item[0] for item in teams.items() if item[1] == team_id][0]


def _get_readable_datetime(timestamp):
    _datetime = datetime.fromisoformat(timestamp)
    return f"{_datetime.strftime('%d %b %H:%M')}"


@app.command()
def main(team: str, results: Annotated[bool, typer.Option()] = False):
    # TODO: handle scenarios for requests caching
    session = CachedSession(".fpl_cache", backend="sqlite")

    teams = _get_teams(session)
    team_id = _get_id_from_team(team, teams)

    fixtures = _get_fixtures(session)

    team_fixtures = [
        fixture
        for fixture in fixtures
        if fixture["team_h"] == team_id or fixture["team_a"] == team_id
    ]
    if results:
        recent_fixtures = [fixture for fixture in team_fixtures if fixture["finished"]][
            -5:
        ]
        if len(recent_fixtures) == 0:
            raise NoFixturesError(f"No recent fixtures found for '{team}'")
        typer.echo("Results:")
        for fixture in recent_fixtures:
            fixture_string = f"- {_get_team_from_id(fixture['team_h'], teams)} {fixture['team_h_score']} {_get_team_from_id(fixture['team_a'], teams)} {fixture['team_a_score']}, {_get_readable_datetime(fixture['kickoff_time'])}"
            typer.echo(fixture_string)
    else:
        upcoming_fixtures = [
            fixture for fixture in team_fixtures if not fixture["finished"]
        ][:5]
        if len(upcoming_fixtures) == 0:
            raise NoFixturesError(f"No upcoming fixtures found for '{team}'")
        typer.echo("Upcoming Fixtures:")
        for fixture in upcoming_fixtures:
            fixture_string = f"- {_get_team_from_id(fixture['team_h'], teams)} vs {_get_team_from_id(fixture['team_a'], teams)}, {_get_readable_datetime(fixture['kickoff_time'])}"
            typer.echo(fixture_string)
