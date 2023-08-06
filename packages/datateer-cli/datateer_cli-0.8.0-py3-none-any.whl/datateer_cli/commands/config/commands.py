import click

from .operations import pull_config, push_config

name = "Datateer CLI config commands"


@click.group(help="Commands related to configuration")
def config():
    pass


@config.command(
    help="Pulls configuration down from a Datateer environment and puts it into the configuration directory"
)
@click.option(
    "-d",
    "--config-dir",
    default=".datateer",
    required=True,
    help="will pull the config into this directory and overwrite what is there",
)
@click.option(
    "-p",
    "--aws-profile",
    envvar="AWS_PROFILE",
    required=True,
    help="(defaults to env var AWS_PROFILE)",
)
@click.option(
    "-r",
    "--aws-region",
    envvar="AWS_REGION",
    required=True,
    help="(defaults to env var AWS_REGION)",
)
@click.option(
    "-c",
    "--client-code",
    envvar="CLIENT_CODE",
    required=True,
    help="(defaults to env var CLIENT_CODE)",
)
@click.option(
    "-e",
    "--environment",
    envvar="DATATEER_ENV",
    type=click.Choice(["prod", "stg", "qa", "int"], case_sensitive=False),
    required=True,
    help="The target Datateer environment (defaults to env var DATATEER_ENV)",
)
def pull(config_dir, aws_profile, aws_region, client_code, environment):
    pull_config(config_dir, aws_profile, aws_region, client_code, environment)


@config.command(
    help="Pushes configuration up to a Datateer environment from the configuration directory"
)
@click.option(
    "-d",
    "--config-dir",
    default=".datateer",
    required=True,
    help="will pull the config into this directory and overwrite what is there",
)
@click.option(
    "-p",
    "--aws-profile",
    envvar="AWS_PROFILE",
    required=True,
    help="(defaults to env var AWS_PROFILE)",
)
@click.option(
    "-r",
    "--aws-region",
    envvar="AWS_REGION",
    required=True,
    help="(defaults to env var AWS_REGION)",
)
@click.option(
    "-c",
    "--client-code",
    envvar="CLIENT_CODE",
    required=True,
    help="(defaults to env var CLIENT_CODE)",
)
@click.option(
    "-e",
    "--environment",
    envvar="DATATEER_ENV",
    type=click.Choice(["prod", "stg", "qa", "int"], case_sensitive=False),
    required=True,
    help="The target Datateer environment (defaults to env var DATATEER_ENV)",
)
def push(config_dir, aws_profile, aws_region, client_code, environment):
    push_config(config_dir, aws_profile, aws_region, client_code, environment)
