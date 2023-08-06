#!/usr/bin/env python3
import pytest
from .context import *

FIRST_KEY='install'

@pytest.fixture
def y():
    return ymm.load_file(TEST_FILE)

def test_load(y):
    assert y
    assert y.yaml
    assert y.yaml[FIRST_KEY]

def test_run(y):
    result = y.run(FIRST_KEY)
    assert FIRST_KEY in result[0]
