"""
Concevez le jeu du démineur en version console. Le but du jeu est de détecter des mines
placées aléatoirement dans un champ de mines en y posant un drapeau. Concevez ce
projet en TDD avec Pytest. Vous pouvez utiliser des bibliothèques tierce (comme tabulate
et colorama) pour l’interface graphique.
Faites en sorte de ne pas tomber sur une mine dès la première case
__author__ = Gvanderveen
__version__ = 0.1
"""

from tabulate import tabulate
from random import randrange
from numpy import full, ndenumerate, count_nonzero, random


def init_board(sizex: int, sizey: int) -> list:
    """
    Take a sizex and sizey argument and create a nparray sizex x sizey
    """
    return full((sizey, sizex), -1)


def show_board(board: list) -> None:
    """
    Print the board
    """
    print(tabulate(board, tablefmt="simple_grid"))


def get_usrin() -> tuple:
    """
    return a tuple with (row,col)
    """
    coord = int(input("ligne ? ")), int(input("collone ? "))
    return coord


def generate_bombs(board, nbr) -> list:
    """
    create nbr bombs in the board
    """
    bombs_added = 0
    if count_nonzero(board == -1) < nbr:
        return board
    while nbr != bombs_added:
        rdm_y = randrange(0, len(board))
        rdm_x = randrange(0, len(board[0]))
        if board[rdm_y, rdm_x] == -1:
            board[rdm_y, rdm_x] = 9
            bombs_added += 1
    return board


def create_numbers(board):
    """
    add the number of bomb arround in each cell
    """
    for it, x in ndenumerate(board):
        if board[it] != 9:
            x_min = it[1] - 1 if it[1] - 1 > 0 else 0
            x_max = it[1] + 2 if it[1] + 2 < len(board[it[0]]) else len(board[it[0]])
            y_min = it[0] - 1 if it[0] - 1 > 0 else 0
            y_max = it[0] + 2 if it[0] + 2 < len(board) + 1 else len(board) + 1
            board[it] = count_nonzero(board[y_min:y_max, x_min:x_max] == 9)
    return board



def make_group(board, coord):
    """ """
    oui=[]
    for it, x in ndenumerate(board):
        if x == 0:
            

        
        

def main():
    """"""


if __name__ == "__main__":
    oui = init_board(5, 5)
    generate_bombs(oui, 3)
    create_numbers(oui)
    show_board(oui)
