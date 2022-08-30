import logging
import click

from ..utils.core import Container, get_function_name

TEST_COMMAND_KEY = "test_command"

@click.command()
@click.pass_context
def test_command(ctx: click.Context) -> None:
    """Click command to test command.
    \f

    Args:
        ctx (object): Click Context object supplied by caller
    """
    click.echo(f"Executing command: {get_function_name()}...")
    click.echo(f"Context is: {ctx.obj.get('CONFIG', '')}")

    container = Container()

    config = container.config

    config.from_yaml(ctx.obj["CONFIG"])

    # Override logfile
    config.default.logfile.override(config.get(f"{TEST_COMMAND_KEY}.logfile"))

    container.core.init_resources()

    logger = logging.getLogger(get_function_name())

    logger.info("Running test command!")

    click.echo("Done!")
