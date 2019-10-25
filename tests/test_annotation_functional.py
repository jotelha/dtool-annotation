"""Functional test of 'dtool annotation' CLI command."""

from click.testing import CliRunner

from . import tmp_dataset_fixture  # NOQA


def test_annotation_basic(tmp_dataset_fixture):  # NOQA

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


def test_annotation_invalid_name(tmp_dataset_fixture):  # NOQA

    from dtool_annotation.cli import annotation

    runner = CliRunner()

    # Spaces, slashes, etc are not allowed.
    result = runner.invoke(annotation, [
        "set",
        tmp_dataset_fixture.uri,
        "project name",
        "world-peace"
    ])
    assert result.exit_code == 400

    expected_lines = [
        "Invalid annotation name 'project name'",
        "Name must be 80 characters or less",
        "Names may only contain the characters: 0-9 a-z A-Z - _ .",
        "Example: citation-index",
    ]
    for line in expected_lines:
        assert result.output.find(line) != -1



def test_get_non_existing_annotation(tmp_dataset_fixture):  # NOQA

    from dtool_annotation.cli import annotation

    runner = CliRunner()

    result = runner.invoke(annotation, [
        "get",
        tmp_dataset_fixture.uri,
        "project",
    ])
    assert result.exit_code == 401
    expected = "No annotation named: 'project'"
    assert result.output.strip() == expected
