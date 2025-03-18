import pytest
from typer.testing import CliRunner

import fixtures.main
from fixtures.main import InvalidTeamError, NoFixturesError, app

runner = CliRunner()


@pytest.fixture
def mock_teams(monkeypatch):
    def mock_get_teams(*args, **kwargs):
        return {
            "London": 1,
            "Glasgow": 2,
            "Cardiff": 3,
            "Belfast": 4,
            "Edinburgh": 5,
        }

    monkeypatch.setattr(fixtures.main, "_get_teams", mock_get_teams)


@pytest.fixture
def mock_fixtures(monkeypatch):
    def mock_get_fixtures(*args, **kwargs):
        return [
            {
                "finished": True,
                "team_h": 1,
                "team_h_score": 0,
                "team_a": 2,
                "team_a_score": 0,
                "kickoff_time": "2025-01-01T09:00:00Z",
            },
            {
                "finished": True,
                "team_h": 3,
                "team_h_score": 2,
                "team_a": 1,
                "team_a_score": 1,
                "kickoff_time": "2025-02-01T12:00:00Z",
            },
            {
                "finished": False,
                "team_h": 1,
                "team_h_score": None,
                "team_a": 4,
                "team_a_score": None,
                "kickoff_time": "2025-03-01T15:00:00Z",
            },
            {
                "finished": False,
                "team_h": 2,
                "team_h_score": None,
                "team_a": 1,
                "team_a_score": None,
                "kickoff_time": "2025-04-01T18:00:00Z",
            },
        ]

    monkeypatch.setattr(fixtures.main, "_get_fixtures", mock_get_fixtures)


def test_fixtures(mock_teams, mock_fixtures):
    result = runner.invoke(app, ["London"])
    assert result.exit_code == 0
    assert "Upcoming Fixtures:" in result.stdout
    assert "- London vs Belfast, 01 Mar 15:00" in result.stdout
    assert "- Glasgow vs London, 01 Apr 18:00" in result.stdout


def test_valid_results(mock_teams, mock_fixtures):
    result = runner.invoke(app, ["London", "--results"])
    assert result.exit_code == 0
    assert "Results:" in result.stdout
    assert "- London 0 Glasgow 0, 01 Jan 09:00" in result.stdout
    assert "- Cardiff 2 London 1, 01 Feb 12:00" in result.stdout


def test_invalid_team(mock_teams, mock_fixtures):
    result = runner.invoke(
        app,
        ["NotLondon"],
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, InvalidTeamError)


def test_no_fixtures(mock_teams, mock_fixtures):
    result = runner.invoke(app, ["Edinburgh"])
    assert result.exit_code == 1
    assert isinstance(result.exception, NoFixturesError)


def test_no_results(mock_teams, mock_fixtures):
    result = runner.invoke(app, ["Edinburgh", "--results"])
    assert result.exit_code == 1
    assert isinstance(result.exception, NoFixturesError)
