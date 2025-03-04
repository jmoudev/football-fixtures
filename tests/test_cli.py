from typer.testing import CliRunner

from fixtures.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["Liverpool"])
    assert result.exit_code == 0
    assert "Upcoming Fixtures:" in result.stdout
