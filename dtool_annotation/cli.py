"""dtool annotation CLI commands."""

import dtoolcore
import click

from dtool_cli.cli import base_dataset_uri_argument


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
    click.secho(str(dataset.get_annotation(key)))
