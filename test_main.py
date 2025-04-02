"""
tets for main.py
__author__ = Gvanderveen
__version__ = 0.1
"""

import main


def test_init_empty_board():
    assert main.init_board(5, 5) == [[-1 for _ in range(5)] for _ in range(5)]
