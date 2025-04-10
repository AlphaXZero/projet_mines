"""
Concevez le jeu du démineur en version console. Le but du jeu est de détecter des mines
placées aléatoirement dans un champ de mines en y posant un drapeau. Concevez ce
projet en TDD avec Pytest. Vous pouvez utiliser des bibliothèques tierce (comme tabulate
et colorama) pour l’interface graphique.
Faites en sorte de ne pas tomber sur une mine dès la première case
__author__ = Gvanderveen
__version__ = 0.1
"""

from random import randrange
from tabulate import tabulate
from numpy import full, ndenumerate, count_nonzero, insert, arange, reshape
from colorama import init, Fore, Back, Style

DIRECTIONS = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
GAME_DIFFICULTY = {1: ((8, 10), 10), 2: ((14, 20), 40), 3: ((22, 24), 99)}
COLORS = {
    "0": Back.WHITE,
    "1": Fore.BLUE,
    "2": Fore.GREEN,
    "3": Fore.YELLOW,
    "4": Fore.RED,
    "5": Fore.MAGENTA,
    "6": Fore.CYAN,
    "7": Fore.GREEN,
    "8": Back.YELLOW,
    "9": Back.RED,
}
flag_list = []


def init_board(difficulty) -> list:
    """
    Take a sizex and sizey argument and create a nparray sizex x sizey with 0 if zero is True else -1
    """
    return full(GAME_DIFFICULTY[difficulty][0], -1)


def show_board(board: list, flag: bool | tuple = False) -> None:
    """
    Print the board
    """
    global flag_list
    init()
    board = board.astype(str)

    for it, cell in ndenumerate(board):
        if cell == "-1":
            board[it] = ""
        else:
            board[it] = f"{COLORS[cell]}{cell}{Style.RESET_ALL}"
    board = insert(board, 0, arange(board.shape[1]).astype(str), axis=0)
    board = insert(board, 0, arange(-1, board.shape[0] - 1).astype(str), axis=1)
    if flag:
        if 0 <= flag[0] + 1 <= board.shape[1] and 0 <= flag[1] + 1 <= board.shape[0]:
            if (flag[1] + 1, flag[0] + 1) in flag_list:
                flag_list.remove((flag[1] + 1, flag[0] + 1))
            else:
                flag_list.append((flag[1] + 1, flag[0] + 1))
    for cell in flag_list:
        board[cell] = f"{Back.RED}/>{Style.RESET_ALL}"
    print(tabulate(board, tablefmt="simple_grid"))
    return board


def get_usrin(board: list) -> tuple[int]:
    """
    ask row and col and return a tuple
    """
    while True:
        coord = input(
            "Entrez la colonne puis la ligne séparé par 1 espace \nMettez "
            "f suivi d'un espace avant de mettre la colonne pour mettre un flag \nx pour quitter : "
        ).split(" ")
        if "x" in coord:
            quit()
        flag = True if len(coord) == 3 and coord[0] in ("f", "F") else False
        if flag:
            coord = coord[1:]
        if len(coord) == 2 and coord[0].isdigit() and coord[1].isdigit():
            if flag:
                show_board(board, (int(coord[0]), int(coord[1])))
            else:
                return int(coord[0]), int(coord[1])


def get_adjacent_list(board: list, coord: tuple[int]) -> list[tuple[int]]:
    """
    return a list with every cells around the coord
    """
    y_min, y_max, x_min, x_max = get_adjacent_coord(board, coord)
    return board[y_min:y_max, x_min:x_max]


def get_adjacent_coord(board: list, coord: tuple[int]) -> tuple[int]:
    """
    return a tuple with the index of intervals around the coord
    (y_min,y_max,x_min,x_max)
    """
    x_min = max(0, coord[1] - 1)
    x_max = min(len(board[coord[0]]), coord[1] + 2)
    y_min = max(0, coord[0] - 1)
    y_max = min(len(board) + 1, coord[0] + 2)
    return (x_min, x_max, y_min, y_max)


def generate_bombs(board: list, nbr: int, usr_choice: tuple[int]) -> list:
    """
    init nbr bombs in the board where not around the usr_choice SAMPLE
    """
    adjacent_tiles = get_adjacent_coord(board, usr_choice)
    adjacent_tiles_list = [
        (i, j)
        for i in range(adjacent_tiles[0], adjacent_tiles[1])
        for j in range(adjacent_tiles[2], adjacent_tiles[3])
    ]
    index_list = []
    for it, _ in ndenumerate(board):
        if it not in adjacent_tiles_list:
            index_list.append(it)
    for i in range(nbr):
        board[index_list.pop(randrange(0, len(index_list)))] = 9
    return board


def create_numbers(board: list) -> list:
    """
    add the number of bomb arround in each cell
    """
    for it, _ in ndenumerate(board):
        if board[it] != 9:
            y_min, y_max, x_min, x_max = get_adjacent_coord(board, it)
            board[it] = count_nonzero(board[y_min:y_max, x_min:x_max] == 9)
    return board


def make_group(board: list, coord: tuple[int]) -> list[tuple[int]]:
    """
    return a list of every cell that have to be revealed
    """
    index_to_check = [coord] if board[coord] == 0 else []
    index_list = [coord]
    while len(index_to_check) > 0:
        new_y, new_x = index_to_check.pop()
        for y, x in DIRECTIONS:
            neww_y, neww_x = new_y + y, new_x + x
            if 0 <= neww_y < board.shape[0] and 0 <= neww_x < board.shape[1]:
                if board[neww_y, neww_x] == 0 and (neww_y, neww_x) not in index_list:
                    index_to_check.append((neww_y, neww_x))
                if (neww_y, neww_x) not in index_list and board[(neww_y, neww_x)] != 9:
                    index_list.append((neww_y, neww_x))
    return index_list


def reveal_board(board: list, blank_board: list, index_to_reveal: tuple[int]) -> list:
    """
    add every board[index_to_reveal] in the blank_board
    """
    for i in index_to_reveal:
        blank_board[i] = board[i]
    return blank_board


def compare_boards(
    blank_board: list, board: list, coord: tuple[int], game_diffculty
) -> int:
    """
    return a int for different case
    -1 -> loose
    0 -> already reveal
    1 -> ok
    """
    coord = coord[1], coord[0]
    if board[coord] == 9:
        return -1
    if count_nonzero(blank_board == -1) == GAME_DIFFICULTY[game_diffculty][1]:
        return 2
    if board[coord] == blank_board[coord]:
        return 0
    else:
        return 1


def get_settings():
    """"""
    while True:
        game_diff = input(
            "Choissisez un niveau de diffciulté 1 facile 2 moyen 3 difficile : "
        )
        if game_diff in ("1", "2", "3"):
            return int(game_diff)


# TODO : faire 3 lvls diffcivultés + meilleur input + flag + opti main + 0 en diagonale -> pas révélé normalement solutuiion regardé la la lsite des index ajouté entre haut et droite puis supprimer si 2 int
def main():
    """
    main function for the game
    """
    settings = get_settings()
    board = None
    blank_board = init_board(settings)
    while True:
        show_board(blank_board)
        user_choice = get_usrin(board)

        if board is None:
            board = create_numbers(
                generate_bombs(
                    init_board(settings), GAME_DIFFICULTY[settings][1], user_choice
                )
            )
        cell_spec = compare_boards(blank_board, board, user_choice, settings)
        if cell_spec == 1:
            print(make_group(board, user_choice))
            blank_board = reveal_board(
                board, blank_board, make_group(board, user_choice)
            )
        show_board(board)


if __name__ == "__main__":
    main()
