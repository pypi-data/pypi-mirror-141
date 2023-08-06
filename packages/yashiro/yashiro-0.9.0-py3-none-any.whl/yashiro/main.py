import argparse
import os
from pathlib import Path
from typing import Any, Dict

import jinja2
from dj_settings.utils import FileReader

from yashiro import __version__


class Parser:
    __slots__ = ["template", "mapping"]

    def __init__(self, args: argparse.Namespace):
        extra: Dict[str, Any] = {}
        if args.strict:
            extra["undefined"] = jinja2.StrictUndefined
        with open(args.template) as file:
            self.template = jinja2.Template(file.read(), **extra)
        self.mapping = dict(os.environ)
        mappings_file = args.mappings
        if mappings_file is not None:
            data = FileReader(Path(mappings_file)).data
            self.mapping.update(data.get("yashiro", {}))

    def __call__(self) -> str:
        return self.template.render(self.mapping)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="yashiro",
        description="A utility to manage testing and migrating a database",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print the version and exit",
    )
    parser.add_argument(
        "-m", "--mappings", help="The path to the file that contains the mappings"
    )
    parser.add_argument(
        "-s", "--strict", action="store_true", help="Disallow missing arguments"
    )
    parser.add_argument(
        "-t", "--template", required=True, help="The path to the template"
    )

    return parser.parse_args()


def get_output() -> str:
    args = parse_args()
    parser = Parser(args)
    return parser()


def write_output() -> None:
    print(get_output())
