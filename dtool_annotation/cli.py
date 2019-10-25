"""dtool annotation CLI commands."""

import sys

import dtoolcore
import click

from dtool_cli.cli import base_dataset_uri_argument


def _validate_name(name):
    if not dtoolcore.utils.name_is_valid(name):
        click.secho("Invalid annotation name '{}'".format(name), fg="red")
        click.secho(
            "Name must be 80 characters or less",
        )
        click.secho(
            "Names may only contain the characters: {}".format(
                " ".join(dtoolcore.utils.NAME_VALID_CHARS_LIST)
            ),
        )
        click.secho("Example: citation-index")
        sys.exit(400)


@click.group()
def annotation():
    """Annotations provide per dataset key/value metadata."""


@annotation.command(name="set")
@base_dataset_uri_argument
@click.argument("key")
@click.argument("value")
def set_annotation(dataset_uri, key, value):
    """Set dataset annotation (key/value pair)."""
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=dtoolcore.utils.DEFAULT_CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=dtoolcore.utils.DEFAULT_CONFIG_PATH
        )

    _validate_name(key)
    dataset.put_annotation(key, value)


@annotation.command(name="get")
@base_dataset_uri_argument
@click.argument("key")
def get_annotation(dataset_uri, key):
    """Get dataset annotation (value associated with the input key)."""
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=dtoolcore.utils.DEFAULT_CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=dtoolcore.utils.DEFAULT_CONFIG_PATH
        )
    try:
        click.secho(str(dataset.get_annotation(key)))
    except dtoolcore.DtoolCoreKeyError:
        click.secho(
            "No annotation named: '{}'".format(key),
            err=True,
            fg="red"
        )
        sys.exit(401)
