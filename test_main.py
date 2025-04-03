"""
tets for main.py
__author__ = Gvanderveen
__version__ = 0.1
"""

import main
import pytest
import numpy as np


@pytest.fixture
def rand_width():
    return np.random.randint(5, 20)


@pytest.fixture
def rand_height():
    return np.random.randint(5, 20)


@pytest.mark.loop(10)
def test_init_empty_board(rand_width, rand_height):
    board = main.init_board(rand_width, rand_height)
    a, b = board.shape
    assert b == rand_width
    assert a == rand_height
