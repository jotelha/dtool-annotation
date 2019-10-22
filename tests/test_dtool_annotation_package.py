"""Test the dtool_annotation package."""


def test_version_is_string():
    import dtool_annotation
    assert isinstance(dtool_annotation.__version__, str)
