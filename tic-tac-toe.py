from enum import Enum
import sys

states = {
    "u_cell": None,
    "x_cell": True,
    "o_cell": False,
}


class CheckMethodType(Enum):
    MATRIX = "matrix"
    TREE = "tree"
    @classmethod
    def _missing_(cls, value):
        return cls.TREE


is_finite_field = True
sign_sequence_limit = 3
chosen_check_method = CheckMethodType.TREE

messages = {
    "ENTER_COORDS": "Введите координаты ряда и колонки через запятую:",
    "WRONG_COORDS": "Выбранное Вами поле занято, введите корректные координаты...",
    "INPUT_FINISHING_METHOD": "Введите желаемый алгоритм проверки выйгрыша (matrix/tree): ",
    "INPUT_WRONG_FINISHING_METHOD": "Неверно, введите корректное значение (matrix/tree): ",
}


def get_field_default_state(col_count, row_count):
    field = []
    for i in range(row_count):
        row = []
        for j in range(col_count):
            row.append(states["u_cell"])
        field.append(row)
    return field


def get_square_field_default_state(size):
    return get_field_default_state(size, size)


def get_cell_view(value):
    value_sign = " "
    if value == states["x_cell"]:
        value_sign = "X"
    elif value == states["o_cell"]:
        value_sign = "O"
    return " " + value_sign + " "


def get_delimiter_cell_view(symbol_count):
    str = ""
    for _ in range(symbol_count):
        str += "-"
    return str


def print_field(field):
    col_count = len(field[0])
    for i in range(len(field)):
        row_string = ""
        delimiter = ""
        for j in range(col_count):
            cell = get_cell_view(field[i][j])
            row_string += ("" if j == 0 else "|") + cell
            delimiter += ("" if j == 0 else "+") + get_delimiter_cell_view(len(cell))
        print(row_string)
        if i < len(field) - 1:
            print(delimiter)


def create_list(size, element):
    list = []
    for _ in range(size):
        list.append(element)
    return list


def process_field(field, callback, params=None):
    row_count = len(field)
    col_count = len(field[0])
    for i in range(row_count):
        for j in range(col_count):
            if callback(field, (i, j), params):
                return True
    return False


def get_matrix_field_processing_callback(field, coords, params):
    # todo fix
    value = field[coords[0]][coords[1]]
    matrix_coords = (params["limit"] - 1 + coords[0] - params["last_coords"][0], params["limit"] - 1 + coords[1] - params["last_coords"][1])
    if matrix_coords[0] >= 0 and matrix_coords[1] >= 0 and matrix_coords[0] < params["limit"] * 2 - 1 and matrix_coords[1] < params["limit"] * 2 - 1:
        params["matrix"][matrix_coords[0]][matrix_coords[1]] = value
    return False


def get_string_from_matrix_by_pattern(matrix, pattern):
    sequence = []
    for coords in pattern:
        sequence.append(matrix[coords[0]][coords[1]])
    output_string = ""
    for item in sequence:
        output_string += transform_item_to_string(item)
    return output_string


def get_size(limit):
    return limit * 2 - 1


def get_patterns_for_matrix(limit):
    patterns_list = [[], [], [], []]
    size = get_size(limit)
    for i in range(size):
        patterns_list[0].append((i, i))             # back slash
        patterns_list[1].append((i, limit - 1))     # vertical
        patterns_list[2].append((i, size - 1 - i))  # slash
        patterns_list[3].append((limit - 1, i))     # horizontal
    return patterns_list


def is_finishing_by_matrix(field, last_coords, limit):
    size = get_size(limit)
    row = create_list(size, states["u_cell"])
    matrix = create_list(size, row.copy())
    process_field(field, get_matrix_field_processing_callback,
                  {"matrix": matrix, "last_coords": last_coords, "limit": limit})
    for p in get_patterns_for_matrix(limit):
        string_by_pattern = "".join(get_string_from_matrix_by_pattern(matrix, p))
        if "X" * limit in string_by_pattern or "O" * limit in string_by_pattern:
            return True
    return False


def get_value_from_field_safe(field, coords):
    try:
        return field[coords[0]][coords[1]]
    except IndexError:
        return states["u_cell"]


def transform_item_to_string(item):
    if item == states["o_cell"]:
        return "O"
    elif item == states["x_cell"]:
        return "X"
    else:
        return "U"


def get_strings_for_tree(field, last_coords, limit):
    strings_set = ["", "", "", ""]
    length = get_size(limit)
    coords_diff = last_coords[0] - last_coords[1]
    loop_diff = int((length - 1)/2)
    for i in range(-1 * loop_diff, loop_diff + 1):
        strings_set[0] += transform_item_to_string(get_value_from_field_safe(field, (last_coords[0] + i, last_coords[0] + i - coords_diff)))
        strings_set[1] += transform_item_to_string(get_value_from_field_safe(field, (last_coords[0] + i, last_coords[1])))
        strings_set[2] += transform_item_to_string(get_value_from_field_safe(field, (-1 * (last_coords[0] + i), last_coords[0] + i - coords_diff)))
        strings_set[3] += transform_item_to_string(get_value_from_field_safe(field, (last_coords[0], last_coords[0] + i - coords_diff)))
    return strings_set


def is_finishing_by_tree(field, last_coords, limit):
    for s in get_strings_for_tree(field, last_coords, limit):
        if "X" * limit in s or "O" * limit in s:
            return True
    return False


def is_field_not_full(field):
    return process_field(field, (lambda f, indices, _: f[indices[0]][indices[1]] == states["u_cell"]))


def is_finishing(field, last_coords, limit):
    if chosen_check_method == CheckMethodType.TREE:
        return not is_finishing_by_tree(field, last_coords, limit)
    elif chosen_check_method == CheckMethodType.MATRIX:
        return not is_finishing_by_matrix(field, last_coords, limit)


def is_game_not_finished(field, last_coords):
    if is_field_not_full(field) if is_finite_field else True:
        return is_finishing(field, last_coords, sign_sequence_limit)
    else:
        return False


def put_value(field, row_index, col_index, new_value):
    if field[row_index][col_index] == states["u_cell"]:
        field[row_index][col_index] = new_value
        return True
    return False


def put_player_input(field, value):
    input_string = input(messages["ENTER_COORDS"])
    coords = input_string.split(",")
    if put_value(field, int(coords[0]) - 1, int(coords[1]) - 1, value):
        return True, (int(coords[0]) - 1, int(coords[1]) - 1)
    else:
        print(messages["WRONG_COORDS"])
        return False, (int(coords[0]) - 1, int(coords[1]) - 1)


def put_computer_value(field, value):
    coords = (2, 2)
    return (put_value(field, int(coords[0]) - 1, int(coords[1]) - 1, value), (int(coords[0]) - 1, int(coords[1]) - 1))


def init(field_size):
    return get_square_field_default_state(field_size)


def play(field):
    current_value = states["x_cell"]
    turn_counter = 0
    last_coords = (0, 0)
    while is_game_not_finished(field, last_coords):
        turn_counter += 1

        if turn_counter % 2 == 0:
            result = put_computer_value(field, current_value)
            print_field(field)
            last_coords = result[1]
        else:
            result = put_player_input(field, current_value)
            while (result[0] == False):
                result = put_player_input(field, current_value)
            last_coords = result[1]

        current_value = states["x_cell"] if current_value == states["o_cell"] else states["o_cell"]


def setup(args):
    global chosen_check_method
    is_method_correct = lambda a: a == CheckMethodType.TREE or a == CheckMethodType.MATRIX
    if len(args) > 1:
        for arg in args[1:]:
            if is_method_correct(arg):
                chosen_check_method = CheckMethodType(arg)
    else:
        user_input = input(messages["INPUT_FINISHING_METHOD"])
        while not is_method_correct(user_input):
            user_input = input(messages["INPUT_WRONG_FINISHING_METHOD"])
        chosen_check_method = CheckMethodType(user_input)


setup(sys.argv)
play(init(3))
