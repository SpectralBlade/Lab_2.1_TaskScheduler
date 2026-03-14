from unittest.mock import MagicMock, patch
from src.classes.task import Task


def test_handle_error(cli, capsys):
    test_msg = "Test error message"
    cli._handle_error(test_msg)
    captured = capsys.readouterr()
    assert test_msg in captured.out


def test_load_sources_from_file_exit(cli, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "exit")
    result = cli.load_sources_from_file()
    assert result is False


def test_run_menu_exit(cli, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "0")
    cli.run_menu()


def test_handle_single_source_invalid_input(cli, monkeypatch, capsys):
    cli.validator.validated_sources = [MagicMock()]
    monkeypatch.setattr('builtins.input', lambda _: "999")
    cli._display_cached_source()
    captured = capsys.readouterr()
    assert "Input error" in captured.out


def test_load_sources_from_file_success(cli, monkeypatch):
    mock_src = MagicMock()

    cli.validator.verify = MagicMock(return_value=True)
    cli.validator.validated_sources = [mock_src]
    cli.validator.fetch_and_display = MagicMock(return_value=[Task(1, "test")])

    with patch('os.path.exists', return_value=True), \
            patch('importlib.util.spec_from_file_location'), \
            patch('importlib.util.module_from_spec') as mock_mod:
        mock_module = MagicMock()
        mock_module.SOURCES = [mock_src]
        mock_mod.return_value = mock_module

        inputs = iter(["mock_sources.py", "exit"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        result = cli.load_sources_from_file()

        assert result is True
        assert mock_src in cli.tasks_cache
        assert len(cli.tasks_cache[mock_src]) == 1


def test_run_menu_display_list(cli, monkeypatch, capsys):
    mock_src = MagicMock()
    mock_src.__class__.__name__ = "TestSource"
    cli.validator.validated_sources = [mock_src]

    inputs = iter(["1", "0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    cli.run_menu()
    captured = capsys.readouterr()
    assert "1. TestSource" in captured.out