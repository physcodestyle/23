states = {
    'u_cell': None,
    'x_cell': True,
    'o_cell': False,
}

is_finite_field = True
sign_sequence_limit = 3

messages = {
    'ENTER_COORDS': 'Введите координаты ряда и колонки через запятую:',
    'WRONG_COORDS': 'Выбранное Вами поле занято, введите корректные координаты...',
}

def get_field_default_state(col_count, row_count):
    field = []
    for i in range(row_count):
        row = []
        for j in range(col_count):
            row.append(states['u_cell'])
        field.append(row)
    return field

def get_square_field_default_state(size):
    return get_field_default_state(size, size)

def get_cell_view(value):
    value_sign = ' '
    if value == states['x_cell']:
        value_sign = 'X'
    elif value == states['o_cell']:
        value_sign = 'O'
    return ' ' + value_sign + ' '

def get_delimiter_cell_view(symbol_count):
    str = ''
    for i in range(symbol_count):
        str += '-'
    return str

def print_field(field):
    col_count = len(field[0])
    for i in range(len(field)):
        row_string = ''
        delimiter = ''
        for j in range(col_count):
            cell = get_cell_view(field[i][j])
            row_string += ('' if j == 0 else '|') + cell
            delimiter += ('' if j == 0 else '+') + get_delimiter_cell_view(len(cell))
        print(row_string)
        if i < len(field) - 1:
            print(delimiter)

def create_list(size, element):
    list = []
    for _ in range(size):
        list.append(element)
    return list

def process_field(field, callback, params = None):
    row_count = len(field)
    col_count = len(field[0])
    for i in range(row_count):
        for j in range(col_count):
            if callback(field, (i, j), params):
                return True
    return False

def get_matrix_field_processing_callback(field, coords, params):
    value = field[coords[0]][coords[1]]
    matrix_coords = (params['limit'] - 1 + coords[0] - params['last_coords'][0], params['limit'] - 1 + coords[1] - params['last_coords'][1])
    if matrix_coords[0] >= 0 and matrix_coords[1] >= 0 and matrix_coords[0] < params['limit'] * 2 - 1 and matrix_coords[1] < params['limit'] * 2 - 1:
        params['matrix'][matrix_coords[0]][matrix_coords[1]] = value
    return False

def get_string_from_matrix_by_pattern(matrix, pattern):
    sequence = []
    for coords in pattern:
        sequence.append(matrix[coords[0]][coords[1]])
    output_string = ""
    for item in sequence:
        if item == states["u_cell"]:
            output_string += "U"
        elif item == states["x_cell"]:
            output_string += "X"
        elif item == states["o_cell"]:
            output_string += "O"

def get_size(limit):
    return limit * 2 - 1

def get_patterns(limit):
    patterns_list = [[], [], [], []]
    size = get_size(limit)
    for i in range(size):
        patterns_list[0].append((i, i))         # back slash
        patterns_list[1].append((i, limit))     # vertical
        patterns_list[2].append((i, size - i))  # slash
        patterns_list[3].append((limit, i))     # horizontal

def is_not_finishing_by_matrix(field, last_coords, limit):
    size = get_size(limit)
    row = create_list(size, states['u_cell'])
    matrix = create_list(size, row.copy())
    process_field(field, get_matrix_field_processing_callback, { "matrix": matrix, "last_coords": last_coords, "limit": limit })
    for p in get_patterns(limit):
        string_by_pattern = ''.join(get_string_from_matrix_by_pattern(matrix, p))
        if 'X' * limit in string_by_pattern or 'O' * limit in string_by_pattern:
            return True
    return False

def is_not_finishing_by_tree(field, last_coords, limit):
    pass

def is_field_full(field):
    return process_field(field, (lambda f, indices, _ : f[indices[0]][indices[1]] == states['u_cell']))

def is_game_not_finished(field, last_coords):
    if (is_field_full(field) if is_finite_field else True):
        return is_not_finishing_by_matrix(field, last_coords, sign_sequence_limit)
    else:
        return False

def put_value(field, row_index, col_index, new_value):
    if field[row_index][col_index] == states['u_cell']:
        field[row_index][col_index] = new_value
        return True
    return False

def put_player_input(field, value):
    input_string = input(messages['ENTER_COORDS'])
    coords = input_string.split(',')
    if put_value(field, int(coords[0]) - 1, int(coords[1]) - 1, value):
        return (True, int(coords[0]) - 1, int(coords[1]))
    else:
        print(messages['WRONG_COORDS'])
        return (False, int(coords[0]) - 1, int(coords[1]))

def put_computer_value(field, value):
    coords = (2,2)
    return (put_value(field, int(coords[0]) - 1, int(coords[1]) - 1, value), (int(coords[0]) - 1, int(coords[1])))

def init(field_size):
    return get_square_field_default_state(field_size)

def play(field):
    current_value = states['x_cell']
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
            while(result[0] == False):
                result = put_player_input(field, current_value)
            last_coords = result[1]

        current_value = states['x_cell'] if current_value == states['o_cell'] else states['o_cell']

play(init(3))
