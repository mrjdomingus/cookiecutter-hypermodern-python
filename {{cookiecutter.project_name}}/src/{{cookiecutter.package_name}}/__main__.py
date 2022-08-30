"""Command-line interface."""
import click
import os

from .commands.test_command import (
    test_command,
)
from .utils.core import find_config_file

DEFAULT_CONFIG = "{{cookiecutter.package_name}}.yaml"
PACKAGE_HOME = "{{cookiecutter.package_name}}".upper() + "_HOME"

__VERSION__ = "1.0"


@click.group()
@click.version_option(version=__VERSION__)
@click.option(
    "--config",
    default=DEFAULT_CONFIG,
    help=f"configuration file, default: {DEFAULT_CONFIG}",
)
@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """{{cookiecutter.friendly_name}}."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    click.echo(f"Env var [{PACKAGE_HOME}]: {os.environ[PACKAGE_HOME]}")
    resolved_config = find_config_file(config, PACKAGE_HOME)
    if resolved_config:
        ctx.obj["CONFIG"] = resolved_config
    else:
        raise ValueError(f"Configuration file {config} not found!")


cli.add_command(test_command)


def main() -> None:
    cli(obj={}, prog_name="{{cookiecutter.project_name}}")  # pragma: no cover


if __name__ == "__main__":
    main()
