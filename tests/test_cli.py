"""CLI tests: commands on unknown ids must fail, not claim success."""

import importlib
import io

import pytest
from rich.console import Console
from typer.testing import CliRunner


@pytest.fixture()
def isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("TODOX_DB_PATH", str(tmp_path / "todox.json"))
    import todox.cli as cli
    import todox.store as store

    importlib.reload(store)
    importlib.reload(cli)
    out = io.StringIO()
    monkeypatch.setattr(cli, "console", Console(file=out, force_terminal=False))
    yield cli.app, out
    importlib.reload(store)
    importlib.reload(cli)


def test_done_unknown_id_fails(isolated):
    app, out = isolated
    result = CliRunner().invoke(app, ["done", "42"])
    assert result.exit_code == 1
    assert "not found" in out.getvalue()


def test_done_known_id_succeeds(isolated):
    app, out = isolated
    runner = CliRunner()
    created = runner.invoke(app, ["add", "Write tests"])
    assert created.exit_code == 0
    result = runner.invoke(app, ["done", "1"])
    assert result.exit_code == 0
    assert "Marked 1 as done" in out.getvalue()
