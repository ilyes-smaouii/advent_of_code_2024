import helpers
import copy

# open file, collect content
le_filename = "../inputs/day_15_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
le_test_input = \
"""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
le_test_input_2 = \
"""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

######
# PART 1
######

ROBOT_CHAR = "@"
EMPTY_CHAR = "."
WALL_CHAR = "#"
BOX_CHAR = "O"
NO_POS = (-1, -1)
MOVES_DICT = {
  "<" : (0, -1),
  ">" : (0, +1),
  "^" : (-1, 0),
  "v" : (+1, 0),
}

def parse_raw_input(raw_input) :
  map, moves = raw_input.split("\n\n")
  map_table = helpers.raw_to_table(map)
  moves_joined = "".join(moves.split("\n"))
  moves_list = [MOVES_DICT[move_str] for move_str in list(moves_joined)]
  return map_table, moves_list

def find_robot(map_table) :
  for row_idx in range(len(map_table)) :
    for col_idx in range(len(map_table[0])) :
      if map_table[row_idx][col_idx] == ROBOT_CHAR :
        return (row_idx, col_idx)
  return NO_POS

def try_moves(map_table, moves_list) :
  _tab_copy = copy.deepcopy(map_table)
  rob_x, rob_y = find_robot(_tab_copy)
  if (rob_x, rob_y) == NO_POS :
    raise Exception("try_moves() error : coudln't find robot !")
  for vec_x, vec_y in moves_list :
    fst_next_x, fst_next_y = rob_x + vec_x, rob_y + vec_y
    next_x, next_y = fst_next_x, fst_next_y
    fst_next_cell = _tab_copy[next_x][next_y]
    next_cell = fst_next_cell
    helpers.print_log_entries("next_cell (pre-w) : " + next_cell, log_cats = "N_C")
    while next_cell != WALL_CHAR :
      helpers.print_log_entries("next_cell (post-w) : " + next_cell, log_cats = "N_C")
      if next_cell == EMPTY_CHAR :
        _tab_copy[fst_next_x][fst_next_y], _tab_copy[next_x][next_y] =\
          _tab_copy[next_x][next_y], _tab_copy[fst_next_x][fst_next_y]
        _tab_copy[rob_x][rob_y], _tab_copy[fst_next_x][fst_next_y] =\
          _tab_copy[fst_next_x][fst_next_y], _tab_copy[rob_x][rob_y]
        rob_x += vec_x
        rob_y += vec_y
        break
      elif next_cell == BOX_CHAR :
        next_x += vec_x
        next_y += vec_y
        next_cell = _tab_copy[next_x][next_y]
      else :
        raise Exception("try_mvoes() error : next_cell should be Box or Empty !")
    # commented out the line below because it slows down the program, drastically
    # helpers.print_log_entries("\n" + str((vec_x, vec_y)) + "\n" + helpers.table_to_raw(_tab_copy), log_cats = "D")
  return _tab_copy

def compute_score(map_table) :
  score = 0
  for row_idx in range(len(map_table)) :
    for col_idx in range(len(map_table[0])) :
      if map_table[row_idx][col_idx] == BOX_CHAR :
        score += 100 * row_idx + col_idx
  return score

le_test_map, le_test_moves = parse_raw_input(le_test_input)
le_test_map_2, le_test_moves_2 = parse_raw_input(le_test_input_2)

helpers.LOG_DICT["T"] = [False, "[TESTING]"]
helpers.LOG_DICT["D"] = [False, "[DEBUG]"]

helpers.print_log_entries("try_moves() on le_test_input :", \
  "\n" + helpers.table_to_raw(try_moves(le_test_map, le_test_moves)), log_cats = {"T"})
helpers.print_log_entries("try_moves() on le_test_input_2 :", \
  "\n" + helpers.table_to_raw(try_moves(le_test_map_2, le_test_moves_2)), log_cats = {"T"})

le_map, le_moves = parse_raw_input(le_file_content)
le_after_table = try_moves(le_map, le_moves)
le_score = compute_score(le_after_table)

helpers.print_log_entries("try_moves() on input :", \
  "\n" + helpers.table_to_raw(le_after_table), log_cats = {"T"})
helpers.print_log_entries("Score for le_after_table :", le_score, log_cats = "R")


######
# PART 2
######

BOX_L = "["
BOX_R = "]"

le_test_input_3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

def get_box_area(map_table, box_pos, move) :
  move_x, move_y = move
  box_x, box_y = box_pos
  final_area = set()
  next_layer = set()
  if map_table[box_x][box_y] == BOX_L :
    next_layer.update({(box_x, box_y), (box_x, box_y + 1)})
  elif map_table[box_x][box_y] == BOX_R :
    next_layer.update({(box_x, box_y), (box_x, box_y - 1)})
  while len(next_layer) > 0 :
    final_area.update(next_layer)
    temp_next_layer = set()
    for x, y in next_layer :
      # Assumption made here that the map is well-formed, i.e. "[" and "]" are always next to each other, in that order
      if map_table[x + move_x][y + move_y] == BOX_L :
        temp_next_layer.update({(x + move_x, y + move_y), (x + move_x, y + move_y + 1)})
      elif map_table[x + move_x][y + move_y] == BOX_R :
        temp_next_layer.update({(x + move_x, y + move_y), (x + move_x, y + move_y - 1)})
    next_layer = temp_next_layer.difference(final_area)
  return final_area

def move_box_area(map_table, box_area, move) :
  vec_x, vec_y = move
  new_group = set()
  for box_x, box_y in box_area :
    new_x, new_y = box_x + vec_x, box_y + vec_y
    if map_table[new_x][new_y] == WALL_CHAR :
      return (False, box_area)
    else :
      new_group.add(((new_x, new_y), map_table[box_x][box_y]))
  return (True, new_group)

def attempt_move(map_table, rob_pos, move) :
  rob_x, rob_y = rob_pos
  move_x, move_y = move
  contact_x, contact_y = rob_x + move_x, rob_y + move_y
  if map_table[contact_x][contact_y] == WALL_CHAR :
    return (map_table, rob_pos)
  box_area = get_box_area(map_table, (contact_x, contact_y), move)
  move_worked, new_box_area = move_box_area(map_table, box_area, move)
  if move_worked :
    for box_x, box_y in box_area :
      map_table[box_x][box_y] = EMPTY_CHAR
    for ((new_box_x, new_box_y), new_char) in new_box_area :
      map_table[new_box_x][new_box_y] = new_char
    map_table[contact_x][contact_y] = ROBOT_CHAR
    map_table[rob_x][rob_y] = EMPTY_CHAR
    new_rob_pos = rob_x + move_x, rob_y + move_y
    return (map_table, new_rob_pos)
  else :
    return (map_table, rob_pos)

def try_moves_wide(map_table, moves) :
  map_table_copy = copy.deepcopy(map_table)
  rob_pos = find_robot(map_table_copy)
  for move in moves :
    map_table_copy, rob_pos = attempt_move(map_table_copy, rob_pos, move)
    # helpers.print_log_entries("\n" + str(move) + " :\n" + helpers.table_to_raw(map_table_copy), log_cats = "D")
  return map_table_copy

def widen_map(map_table) :
  new_map = []
  for line in map_table :
    new_line = []
    for cell in line :
      if cell == WALL_CHAR :
        new_line += [WALL_CHAR, WALL_CHAR]
      elif cell == BOX_CHAR :
        new_line += [BOX_L, BOX_R]
      elif cell == ROBOT_CHAR :
        new_line += [ROBOT_CHAR, EMPTY_CHAR]
      elif cell == EMPTY_CHAR :
        new_line += [EMPTY_CHAR, EMPTY_CHAR]
      else :
        raise Exception("widen_map() error : cell should be Box, Robot or Wall ! (found {} instead)".format(cell))
    new_map.append(new_line)
  return new_map

def compute_wide_score(map_table) :
  score = 0
  for row_idx in range(len(map_table)) :
    for col_idx in range(len(map_table[0])) :
      if map_table[row_idx][col_idx] == BOX_L :
        score += 100 * row_idx + col_idx
  return score

le_widened_test_map = widen_map(le_test_map_2)

helpers.LOG_DICT["T"] = [False, "[TESTING]"]
helpers.LOG_DICT["D"] = [False, "[DEBUG]"]

helpers.print_log_entries("le_widened_test_map :", "\n" + helpers.table_to_raw(le_widened_test_map), log_cats = {"T"})

le_widened_after_test_map = try_moves_wide(le_widened_test_map, le_test_moves_2)
le_wide_test_score = compute_wide_score(le_widened_after_test_map)

helpers.print_log_entries("try_moves_wide() on input :", \
  "\n" + helpers.table_to_raw(le_widened_after_test_map), log_cats = {"T"})
helpers.print_log_entries("Score for le_widened_after_test_map :", le_wide_test_score, log_cats = "T")

le_widened_map = widen_map(le_map)
le_widened_after_map = try_moves_wide(le_widened_map, le_moves)
le_wide_score = compute_wide_score(le_widened_after_map)
helpers.print_log_entries("Score for le_widened_after_table :", le_wide_score, log_cats = "R")