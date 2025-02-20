from argparse import ArgumentParser, Namespace
from typing import Optional


def parse_cli_arguments(
    cli: ArgumentParser, args: Optional[list[str]] = None
) -> Namespace:
    res = cli.parse_args(args)

    if (
        res.ban is None
        and res.audio_preferences is None
        and res.sub_preferences is None
    ):
        cli.error(
            "At least one argument between --ban, --audio-preferences, and --sub-preferences must be specified"
        )

    return res


def build_cli() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "path",
        nargs="+",
        action="extend",
        help="Path to the mkv file or media directory",
    )

    parser.add_argument(
        "--ban",
        nargs="+",
        action="extend",
        help="Languages to remove from the default tracks",
        required=False,
    )

    parser.add_argument(
        "--audio-preferences",
        nargs="+",
        action="extend",
        help="Language preferences for audio tracks",
        required=False,
    )
    parser.add_argument(
        "--sub-preferences",
        nargs="+",
        action="extend",
        help="Language preferences for audio tracks",
        required=False,
    )

    parser.add_argument("--recursive", action="store_true", default=False)

    return parser
