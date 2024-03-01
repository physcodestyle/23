states = {
    'u_cell': None,
    'x_cell': True,
    'o_cell': False,
}

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

def is_game_not_finished(field):
    row_count = len(field)
    col_count = len(field[0])
    for i in range(row_count):
        for j in range(col_count):
            if field[i][j] == states['u_cell']:
                return True
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
        return True
    else:
        print(messages['WRONG_COORDS'])
        return False

def put_computer_value(field, value):
    coords = (2,2)
    put_value(field, int(coords[0]) - 1, int(coords[1]) - 1, value)

def init(field_size):
    return get_square_field_default_state(field_size)

def play(field):
    current_value = states['x_cell']
    turn_counter = 0
    while is_game_not_finished(field):
        turn_counter += 1

        if turn_counter % 2 == 0:
            put_computer_value(field, current_value)
            print_field(field)
        else:
            while(put_player_input(field, current_value) == False):
                pass

        current_value = states['x_cell'] if current_value == states['o_cell'] else states['o_cell']

play(init(3))
