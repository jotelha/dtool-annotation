"""Functional test of 'dtool annotation' CLI command."""

from click.testing import CliRunner

from . import tmp_dataset_fixture  # NOQA


def test_annotation_functional(tmp_dataset_fixture):  # NOQA

    from dtool_annotation.cli import annotation

    runner = CliRunner()

    result = runner.invoke(annotation, [
        "set",
        tmp_dataset_fixture.uri,
        "project",
        "world-peace"
    ])
    assert result.exit_code == 0

    result = runner.invoke(annotation, [
        "get",
        tmp_dataset_fixture.uri,
        "project"
    ])
    assert result.exit_code == 0

    expected = "world-peace"
    actual = result.output.strip()
    assert actual == expected
