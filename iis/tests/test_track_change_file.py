import os.path as op
import shutil

from pytest import fixture

from iis.collector import Collector

here = op.dirname(op.abspath(__file__))

@fixture
def change_file(tmp_path):
    change_file = op.join(here, 'testdata', 'harvested-files.txt')
    tmp_file = op.join(tmp_path, 'test-changes.txt')
    shutil.copy(change_file, tmp_file)
    return tmp_file

def test_track_changes_in_file(change_file):
    collector = Collector()
    line = collector.get_document_and_save_progress(change_file)
    assert line == 'akld0024.xml\n'
    with open(change_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2
        assert lines[0] == 'beth0004.xml\n'
