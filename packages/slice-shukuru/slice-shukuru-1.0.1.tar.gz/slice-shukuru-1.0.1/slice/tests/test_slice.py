import os, glob
from io import BytesIO

import pytest

from slice import slicing

@pytest.fixture
def mockup_data():
    return os.urandom(1024)

def clean_mockup():
    files_to_clean = glob.glob('*.[0-9]')

    for file in files_to_clean:
        os.remove(file)

def test_slice_by_size(mockup_data):
    mockup_file = BytesIO(mockup_data)
    assert slicing.slice_by_size(mockup_file, 'mockup_file', 1024, 256) == 4
    clean_mockup()


def test_slice_by_count(mockup_data):
    mockup_file = BytesIO(mockup_data)
    assert slicing.slice_by_count(mockup_file, 'mockup_file', 1024, 4) == 256
    clean_mockup()

