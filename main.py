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
from numpy import full, ndenumerate, count_nonzero, zeros

DIRECTIONS = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]


def init_board(sizex: int, sizey: int, zero=False) -> list:
    """
    Take a sizex and sizey argument and create a nparray sizex x sizey with 0 if zero is True else -1
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


def generate_bombs(board, nbr, usr_choice) -> list:
    """
    create nbr bombs in the board
    """
    non = get_adjacent(board, usr_choice, index=True)
    print(non)
    bombs_added = 0
    if count_nonzero(board == -1) < nbr:
        return board
    while nbr != bombs_added:
        rdm_y = randrange(0, len(board))
        rdm_x = randrange(0, len(board[0]))
        print(rdm_y, rdm_x)
        if board[rdm_y, rdm_x] == -1 and not (
            non[0] <= rdm_y <= non[1] and non[2] <= rdm_x <= non[3]
        ):
            print("ok")
            board[rdm_y, rdm_x] = 9
            bombs_added += 1
    return board


def get_adjacent(board, coord, index=False):
    x_min = coord[1] - 1 if coord[1] - 1 > 0 else 0
    x_max = (
        coord[1] + 2 if coord[1] + 2 < len(board[coord[0]]) else len(board[coord[0]])
    )
    y_min = coord[0] - 1 if coord[0] - 1 > 0 else 0
    y_max = coord[0] + 2 if coord[0] + 2 < len(board) + 1 else len(board) + 1
    return (
        board[y_min:y_max, x_min:x_max] if not index else [y_min, y_max, x_min, x_max]
    )


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


# TODO : opti
def make_group(board, coord):
    """
    put all the indexs of adjacents 0 and first 0 on the coordinate selected
    """
    index_to_check = [coord]
    reveal = [coord]
    while len(index_to_check) > 0:
        new_y, new_x = index_to_check.pop()
        for y, x in DIRECTIONS:
            neww_y, neww_x = new_y + y, new_x + x
            if 0 <= neww_y < board.shape[0] and 0 <= neww_x < board.shape[1]:
                if board[neww_y, neww_x] == 0 and (neww_y, neww_x) not in reveal:
                    index_to_check.append((neww_y, neww_x))
                if (neww_y, neww_x) not in reveal:
                    reveal.append((neww_y, neww_x))
    return reveal


def reveal_board(board, index_to_reveal):
    """ """
    oui = init_board(board.shape[1], board.shape[0], True)
    for i in index_to_reveal:
        oui[i] = board[i]
    return oui


def main():
    """"""
    blank_board = init_board(5, 5)
    board = init_board(5, 5)
    usr_choice = get_usrin()
    board[usr_choice] = 15
    create_numbers(generate_bombs(board, 5, usr_choice))
    blank_board = reveal_board(board, make_group(board, usr_choice))
    show_board(blank_board)


if __name__ == "__main__":
    main()
    # oui = init_board(5, 5)
    # generate_bombs(oui, 3)
    # create_numbers(oui)    oui = init_board(5, 5)
    # generate_bombs(oui, 3)
    # create_numbers(oui)
    # show_board(oui)

    # reveal_board(oui, make_group(oui, get_usrin()))

    # show_board(oui)

    # reveal_board(oui, make_group(oui, get_usrin()))
