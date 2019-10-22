"""Test fixtures."""

import os
import shutil
import tempfile

import dtoolcore
import pytest

_HERE = os.path.dirname(__file__)


@pytest.fixture
def chdir_fixture(request):
    d = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(d)

    @request.addfinalizer
    def teardown():
        os.chdir(curdir)
        shutil.rmtree(d)


@pytest.fixture
def tmp_dir_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def local_tmp_dir_fixture(request):
    d = tempfile.mkdtemp(dir=_HERE)

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


def create_proto_dataset(base_uri, name, username):
    admin_metadata = dtoolcore.generate_admin_metadata(name, username)
    proto_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=base_uri
    )
    proto_dataset.create()
    proto_dataset.put_readme("")
    return proto_dataset


@pytest.fixture
def tmp_dataset_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)

    proto_dataset = create_proto_dataset(d, "rnaseq", "noone")

    for strain in ("wt", "mut"):
        for read in ("1", "2"):
            fpath = os.path.join(d, "{}{}".format(strain, read))
            with open(fpath, "w") as fh:
                fh.write(read)
            handle = "{}/read_{}.fq.gz".format(strain, read)
            proto_dataset.put_item(fpath, handle)

    md5_fpath = os.path.join(d, "md5.txt")
    with open(md5_fpath, "w") as fh:
        fh.write("")
    md5_handle = "md5.txt"
    proto_dataset.put_item(md5_fpath, md5_handle)

    proto_dataset.freeze()

    return dtoolcore.DataSet.from_uri(proto_dataset.uri)
