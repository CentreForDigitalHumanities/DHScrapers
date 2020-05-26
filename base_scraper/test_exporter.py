import os
import glob
from .exporter import EntityExporter
from .entities.base_entity import BaseEntity

def test_to_xml(tmp_path):
    e1 = BaseEntity()
    e1.prop1 = 'hello'
    e1.prop2 = ['foo', 'bar']
    e1.prop3 = 'girls'
    e2 = BaseEntity()
    e2.prop1 = 'hello again'    
    entities = [ e1, e2 ]
    exporter = EntityExporter(entities)
    
    exporter.to_xml(tmp_path)

    os.chdir(tmp_path)
    files = glob.glob("*.xml")
    assert len(files) == 2
    for file in files:
        with open(file, 'r') as actual:
            if file == str(e1) + '.xml':
                expected_path = get_test_data_path('entity1.xml')
            if file == str(e2) + '.xml':
                expected_path = get_test_data_path('entity2.xml')
            with open(expected_path, 'r') as expected:
                assert actual.read() == expected.read()

def get_test_data_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata', file)
