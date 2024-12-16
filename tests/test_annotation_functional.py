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

    result = runner.invoke(annotation, [
        "delete",
        tmp_dataset_fixture.uri,
        "project"
    ])
    assert result.exit_code == 0

    result = runner.invoke(annotation, [
        "get",
        tmp_dataset_fixture.uri,
        "project"
    ])
    assert result.exit_code != 0
    expected = "No annotation named: 'project'"
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


def test_delete_non_existing_annotation(tmp_dataset_fixture):  # NOQA

    from dtool_annotation.cli import annotation

    runner = CliRunner()

    result = runner.invoke(annotation, [
        "delete",
        tmp_dataset_fixture.uri,
        "project",
    ])
    assert result.exit_code == 0


def test_annotation_types(tmp_dataset_fixture):  # NOQA

    from dtool_annotation.cli import annotation

    runner = CliRunner()

    # Default to string
    result = runner.invoke(annotation, [
        "set",
        tmp_dataset_fixture.uri,
        "one_as_str",
        "1"
    ])
    assert result.exit_code == 0
    assert tmp_dataset_fixture.get_annotation("one_as_str") == "1"

    # Explicit set to string.
    result = runner.invoke(annotation, [
        "set",
        "--type",
        "str",
        tmp_dataset_fixture.uri,
        "one_as_str_explicit",
        "1"
    ])
    assert result.exit_code == 0
    assert tmp_dataset_fixture.get_annotation("one_as_str_explicit") == "1"

    # Explicit set to int.
    result = runner.invoke(annotation, [
        "set",
        "--type",
        "int",
        tmp_dataset_fixture.uri,
        "one_as_int_explicit",
        "1"
    ])
    assert result.exit_code == 0
    assert tmp_dataset_fixture.get_annotation("one_as_int_explicit") == 1

    # Explicit set to float.
    result = runner.invoke(annotation, [
        "set",
        "--type",
        "float",
        tmp_dataset_fixture.uri,
        "one_as_float_explicit",
        "1"
    ])
    assert result.exit_code == 0

    ann = tmp_dataset_fixture.get_annotation("one_as_float_explicit")
    offset = 0.00000001
    assert ann > 1 - offset
    assert ann < 1 + offset
    assert isinstance(ann, float)

    # Explicit set to bool.
    result = runner.invoke(annotation, [
        "set",
        "--type",
        "bool",
        tmp_dataset_fixture.uri,
        "true_as_bool_explicit",
        "1"
    ])
    assert result.exit_code == 0

    ann = tmp_dataset_fixture.get_annotation("true_as_bool_explicit")
    assert ann
    assert isinstance(ann, bool)

    result = runner.invoke(annotation, [
        "set",
        "--type",
        "bool",
        tmp_dataset_fixture.uri,
        "false_as_bool_explicit",
        "0"
    ])
    assert result.exit_code == 0

    ann = tmp_dataset_fixture.get_annotation("false_as_bool_explicit")
    assert not ann
    assert isinstance(ann, bool)

    # Explicit set to json.
    result = runner.invoke(annotation, [
        "set",
        "--type",
        "json",
        tmp_dataset_fixture.uri,
        "json_explicit",
        '{"x": 3, "y": 5}'
    ])
    assert result.exit_code == 0

    ann = tmp_dataset_fixture.get_annotation("json_explicit")
    assert ann == {"x": 3, "y": 5}


def test_ls_command(tmp_dataset_fixture):  # NOQA

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
        "set",
        tmp_dataset_fixture.uri,
        "stars",
        "3",
        "--type",
        "int"
    ])
    assert result.exit_code == 0

    result = runner.invoke(annotation, [
        "set",
        tmp_dataset_fixture.uri,
        "params",
        '{"x": 3}',
        "--type",
        "json"
    ])
    assert result.exit_code == 0

    result = runner.invoke(annotation, [
        "ls",
        tmp_dataset_fixture.uri,
    ])
    assert result.exit_code == 0

    expectations = [
        ("params", "x': 3}"),
        ("project", "world-peace"),
        ("stars", "3")
    ]
    for e, a in zip(expectations, result.output.strip().split("\n")):
        assert a.count("\t") == 1
        assert a.startswith(e[0])
        assert a.endswith(e[1])
