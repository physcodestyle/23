from enum import Enum

class FieldType(Enum):
    FINITE = "finite"
    INFINITE = "infinite"
    
    
    def _missing_(cls, value):
        return cls.INFINITE

    
    def is_finite_field(cls):
        if cls == FieldType.FINITE:
            return True
        elif cls == FieldType.INFINITE:
            return False

class CheckMethodType(Enum):
    MATRIX = "matrix"
    TREE = "tree"
    
    def _missing_(cls, value):
        return cls.TREE

states = {
    "u_cell": None,
    "x_cell": True,
    "o_cell": False,
}

messages = {
    "ENTER_COORDS": "Введите координаты ряда и колонки через запятую:",
    "WRONG_COORDS": "Выбранное Вами поле занято, введите корректные координаты...",
    "GAME_IS_STARTING": "Игра начинается!",
    "GAME_IS_NOT_STARTING": "Игра ещё не началась!",
    "WIN_COMPUTER": "Выиграл компьютер",
    "WIN_PLAYER": "Вы выиграли!",
}

class Field:
    def __init__(self, size, is_finite = False):
        self.field = self.init(size, is_finite)

    
    def init(self, field_size, is_finite):
        if is_finite:
            return self.get_square_field_default_state(field_size)
        else:
            max_size = field_size * 3
            return self.get_square_field_default_state(max_size + max_size % 2 - 1)

    
    def get_row_default_state(self, col_count):
        row = []
        for _ in range(col_count):
            row.append(states["u_cell"])
        return row

    
    def get_field_default_state(self, col_count, row_count):
        field = []
        for _ in range(row_count):
            field.append(self.get_row_default_state(col_count))
        return field

    
    def get_square_field_default_state(self, size):
        return self.get_field_default_state(size, size)
    
    
    def get_cell_view(self, value):
        value_sign = " "
        if value == states["x_cell"]:
            value_sign = "X"
        elif value == states["o_cell"]:
            value_sign = "O"
        return " " + value_sign + " "

    
    def get_delimiter_cell_view(self, symbol_count):
        str = ""
        for _ in range(symbol_count):
            str += "-"
        return str

    
    def get_field(self):
        return self.field


    def print_field(self):
        output = ""
        col_count = len(self.field[0])
        for i in range(len(self.field)):
            row_string = ""
            delimiter = ""
            for j in range(col_count):
                cell = self.get_cell_view(self.field[i][j])
                row_string += ("" if j == 0 else "|") + cell
                delimiter += ("" if j == 0 else "+") + self.get_delimiter_cell_view(len(cell))
            output += row_string
            if i < len(self.field) - 1:
                output += delimiter

class Game:
    def __init__(self, size = 5, is_finite = False, sequence_limit = 5, method = CheckMethodType.TREE, start_value = states["x_cell"]):
        self.field = Field(size, is_finite)
        self.is_finite_field = is_finite
        self.sign_sequence_limit = sequence_limit
        self.chosen_check_method = method
        self.current_value = start_value
        self.last_coords = (0, 0)

    
    def create_list(self, size, element):
        list = []
        for _ in range(size):
            list.append(element)
        return list

    
    def process_field(self, callback, params=None):
        row_count = len(self.field)
        col_count = len(self.field[0])
        for i in range(row_count):
            for j in range(col_count):
                if callback((i, j), params):
                    return True
        return False

    
    def get_matrix_field_processing_callback(self, coords, params):
        # todo fix
        value = self.field[coords[0]][coords[1]]
        matrix_coords = (params["limit"] - 1 + coords[0] - params["last_coords"][0], params["limit"] - 1 + coords[1] - params["last_coords"][1])
        if matrix_coords[0] >= 0 and matrix_coords[1] >= 0 and matrix_coords[0] < params["limit"] * 2 - 1 and matrix_coords[1] < params["limit"] * 2 - 1:
            params["matrix"][matrix_coords[0]][matrix_coords[1]] = value
        return False

    
    def get_string_from_matrix_by_pattern(self, matrix, pattern):
        sequence = []
        for coords in pattern:
            sequence.append(matrix[coords[0]][coords[1]])
        output_string = ""
        for item in sequence:
            output_string += self.transform_item_to_string(item)
        return output_string

    
    def get_size(self, limit):
        return limit * 2 - 1

    
    def get_patterns_for_matrix(self, limit):
        patterns_list = [[], [], [], []]
        size = self.get_size(limit)
        for i in range(size):
            patterns_list[0].append((i, i))             # back slash
            patterns_list[1].append((i, limit - 1))     # vertical
            patterns_list[2].append((i, size - 1 - i))  # slash
            patterns_list[3].append((limit - 1, i))     # horizontal
        return patterns_list

    
    def is_finishing_by_matrix(self, limit):
        size = self.get_size(limit)
        row = self.create_list(size, states["u_cell"])
        matrix = self.create_list(size, row.copy())
        self.process_field(self.get_matrix_field_processing_callback,
                    {"matrix": matrix, "last_coords": self.last_coords, "limit": limit})
        for p in self.get_patterns_for_matrix(limit):
            string_by_pattern = "".join(self.get_string_from_matrix_by_pattern(matrix, p))
            if "X" * limit in string_by_pattern or "O" * limit in string_by_pattern:
                return True
        return False

    
    def get_value_from_field_safe(self, coords):
        try:
            return self.field.field[coords[0]][coords[1]]
        except IndexError:
            return states["u_cell"]

    
    def transform_item_to_string(self, item):
        if item == states["o_cell"]:
            return "O"
        elif item == states["x_cell"]:
            return "X"
        else:
            return "U"

    
    def get_strings_for_tree(self, limit):
        strings_set = ["", "", "", ""]
        length = self.get_size(limit)
        coords_diff = self.last_coords[0] - self.last_coords[1]
        loop_diff = int((length - 1)/2)
        for i in range(-1 * loop_diff, loop_diff + 1):
            strings_set[0] += self.transform_item_to_string(self.get_value_from_field_safe((self.last_coords[0] + i, self.last_coords[0] + i - coords_diff)))
            strings_set[1] += self.transform_item_to_string(self.get_value_from_field_safe((self.last_coords[0] + i, self.last_coords[1])))
            strings_set[2] += self.transform_item_to_string(self.get_value_from_field_safe((-1 * (self.last_coords[0] + i), self.last_coords[0] + i - coords_diff)))
            strings_set[3] += self.transform_item_to_string(self.get_value_from_field_safe((self.last_coords[0], self.last_coords[0] + i - coords_diff)))
        return strings_set

    
    def is_finishing_by_tree(self, limit):
        for s in self.get_strings_for_tree(limit):
            if "X" * limit in s or "O" * limit in s:
                return True
        return False


    
    def is_field_not_full(self):
        return self.process_field((lambda f, indices, _: f[indices[0]][indices[1]] == states["u_cell"]))


    
    def is_finishing(self, limit):
        if self.chosen_check_method == CheckMethodType.TREE:
            return not self.is_finishing_by_tree(limit)
        elif self.chosen_check_method == CheckMethodType.MATRIX:
            return not self.is_finishing_by_matrix(limit)

    
    def is_game_not_finished(self):
        if self.is_field_not_full() if self.is_finite_field else True:
            return self.is_finishing(self.sign_sequence_limit)
        else:
            return False

    
    def put_value(self, row_index, col_index, new_value):
        if self.field.field[row_index][col_index] == states["u_cell"]:
            self.field.field[row_index][col_index] = new_value
            return True
        return False

    
    def put_player_input(self, coords):
        if self.put_value(int(coords[0]) - 1, int(coords[1]) - 1, self.current_value):
            return True, (int(coords[0]) - 1, int(coords[1]) - 1)
        else:
            print(messages["WRONG_COORDS"])
            return False, (int(coords[0]) - 1, int(coords[1]) - 1)

    
    def put_computer_value(self):
        coords = (3, 3)
        return (self.put_value(int(coords[0]) - 1, int(coords[1]) - 1, self.current_value), (int(coords[0]) - 1, int(coords[1]) - 1))

    
    def increase_field(self, limit):
        field_size = len(self.field)
        vertical_frame = self.get_row_default_state(limit)
        for row_index in range(field_size):
            self.field[row_index] = vertical_frame.copy() + self.field[row_index] + vertical_frame.copy()
        horizontal_frame = self.get_field_default_state(field_size + limit * 2, limit)
        return horizontal_frame.copy() + self.field.copy() + horizontal_frame.copy()

    
    def setup_request(self, callback, request_message, wrong_message):
        user_input = input(request_message)
        while not callback(user_input):
            user_input = input(wrong_message)
        return user_input


    def manage_game_after_turn(self):
        field_size = len(self.field.field)
        if not self.is_finite_field and (self.last_coords[0] <= 1 or self.last_coords[0] >= field_size - 2 or self.last_coords[1] <= 1 or self.last_coords[1] >= field_size - 2):
            self.field = self.increase_field(self.sign_sequence_limit)
        self.current_value = states["x_cell"] if self.current_value == states["o_cell"] else states["o_cell"]


    def make_turn(self, coords):
        player_number = 0
        isGameNotFinished = self.is_game_not_finished()
        if isGameNotFinished:
            result = self.put_player_input(coords)
            if (result[0] == False):
                return (result[0], self.field.get_field(), isGameNotFinished, messages["WRONG_COORDS"])
            else:
                self.last_coords = result[1]
            if self.is_game_not_finished():
                self.manage_game_after_turn()
            else:
                return (True, self.field.get_field(), False, messages["WIN_PLAYER"])
            
            result = self.put_computer_value()
            self.last_coords = result[1]
            if self.is_game_not_finished():
                self.manage_game_after_turn()
                player_number = 1
            else:
                return (True, self.field.get_field(), False, messages["WIN_COMPUTER"])
            
            return (True, self.field.get_field(), True, messages["ENTER_COORDS"])
        else:
            return (False, self.field.get_field(), isGameNotFinished, messages["WIN_PLAYER"] if player_number == 0 else messages["WIN_COMPUTER"])
