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
    # TO DO: test that the `harvested-files.txt` tmp file produces xmls
