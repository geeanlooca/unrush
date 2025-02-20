from argparse import ArgumentParser

import pytest

from unrush.cli import build_cli, parse_cli_arguments


@pytest.fixture()
def cli() -> ArgumentParser:
    return build_cli()


def test_build_cli():
    cli = build_cli()


def test_parse_cli_arguments(cli: ArgumentParser) -> None:
    args = ["path", "--ban", "1", "s", "1111"]
    result = cli.parse_args(args)

    with pytest.raises(SystemExit):
        args = ["path", "--ban"]
        _ = parse_cli_arguments(cli, args)

    with pytest.raises(SystemExit):
        args = ["path", "--audio-preferences"]
        _ = parse_cli_arguments(cli, args)

    with pytest.raises(SystemExit):
        args = ["path", "--sub-preferences"]
        _ = parse_cli_arguments(cli, args)

    args = ["path"]
    with pytest.raises(SystemExit):
        _ = parse_cli_arguments(cli, args)

    args = [
        "path",
        "--ban",
        "ru",
        "--audio-preferences",
        "original",
        "italian",
        "--ban",
        "ko",
    ]
    result = parse_cli_arguments(cli, args)

    assert result.ban == ["ru", "ko"]
    assert result.audio_preferences == ["original", "italian"]

    args = ["path", "second_path", "filename.mkv", "--ban", "it"]
    result = parse_cli_arguments(cli, args)
    assert result.path == args[:3]
    assert result.ban == ["it"]
    assert result.audio_preferences is None
    assert result.sub_preferences is None
