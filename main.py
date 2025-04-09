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
from numpy import full, ndenumerate, count_nonzero, insert, arange
from colorama import init, Fore, Back, Style

DIRECTIONS = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
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


def init_board(sizex: int, sizey: int) -> list:
    """
    Take a sizex and sizey argument and create a nparray sizex x sizey with 0 if zero is True else -1
    """
    return full((sizey, sizex), -1)


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
            "Entrez la collone puis la ligne séparé par 1 espace \nMettez "
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
    return (y_min, y_max, x_min, x_max)


def generate_bombs(board: list, nbr: int, usr_choice: tuple[int]) -> list:
    """
    init nbr bombs in the board where not around the usr_choice
    """
    non = get_adjacent_coord(board, usr_choice)
    bombs_added = 0
    while nbr != bombs_added:
        rdm_y, rdm_x = randrange(0, len(board)), randrange(0, len(board[0]))
        if board[rdm_y, rdm_x] == -1 and not (
            non[0] <= rdm_y <= non[1] and non[2] <= rdm_x <= non[3]
        ):
            board[rdm_y, rdm_x] = 9
            bombs_added += 1
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


def compare_boards(blank_board: list, board: list, coord: tuple[int]) -> int:
    """
    return a int for different case
    -1 -> loose
    0 -> already reveal
    1 -> ok
    """
    coord = coord[1], coord[0]
    if board[coord] == 9:
        return -1
    if board[coord] == blank_board[coord]:
        return 0
    else:
        return 1


# TODO : faire 3 lvls diffcivultés + meilleur input + flag + opti main + 0 en diagonale -> pas révélé normalement solutuiion regardé la la lsite des index ajouté entre haut et droite puis supprimer si 2 int
def main():
    """
    main function for the game
    """
    blank_board = init_board(8, 8)
    board = init_board(8, 8)
    show_board(blank_board)
    usr_choice = get_usrin(blank_board)

    create_numbers(generate_bombs(board, 7, usr_choice))
    blank_board = reveal_board(board, blank_board, make_group(board, usr_choice))
    show_board(blank_board)
    while True:
        usr_choice = get_usrin(blank_board)
        check_cell = compare_boards(blank_board, board, usr_choice)
        print(check_cell)
        if check_cell == 1:
            blank_board = reveal_board(
                board, blank_board, make_group(board, usr_choice)
            )
            show_board(blank_board)
        elif check_cell == 0:
            print("case déjà révélé, réessayez ")
        else:
            show_board(board)
            print(Fore.RED + "Perdu")
            exit()


if __name__ == "__main__":
    main()
