import copy

# open file, collect content
le_filename = "day_06_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()
# le_file_content = \
#   """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#..."""

######
# PART 1
######

guard_char = '^'
obstacle_char = '#'
candidate_obstacle_char = "O"
marked_char = 'X'

le_lines = le_file_content.split("\n")
le_row_count = len(le_lines)
le_col_count = len(le_lines[0])

le_board_table = []
le_initial_guard_pos = (0,0)
le_initial_direction = (-1,0)

def get_rotated_90(direction) :
  return (direction[1], -direction[0])

def print_map(board_table) :
  for line in board_table :
    for cell in line :
      print(cell, sep = "", end = "")
    print("\n", sep = "", end = "")

le_obstacles_positions = set()
le_visited_positions = []

# First, read map and store relevant data
for row_idx in range(le_row_count) :
  le_board_table.append([])
  for col_idx in range(le_col_count) :
    cell_content = le_lines[row_idx][col_idx]
    le_board_table[row_idx].append(cell_content)
    if cell_content == guard_char :
      le_initial_guard_pos = (row_idx, col_idx)
    if cell_content == obstacle_char :
      le_obstacles_positions.add(((row_idx, col_idx)))
    pass

def get_visited_positions(initial_guard_pos, initial_direction, obstacle_positions, board_table):
  visited_positions = set()
  row_count = len(board_table)
  col_count = len(board_table[0])
  # then, move guard according to given rules, until it's out
  while 0 <= initial_guard_pos[0] < row_count and 0 <= initial_guard_pos[1] < col_count :
    # keep track of visited positions
    if initial_guard_pos not in visited_positions :
      visited_positions.add(initial_guard_pos)
      board_table[initial_guard_pos[0]][initial_guard_pos[1]] = marked_char
    next_pos = (initial_guard_pos[0] + initial_direction[0], initial_guard_pos[1] + initial_direction[1])
    if next_pos in obstacle_positions :
      initial_direction = get_rotated_90(initial_direction)
    else :
      initial_guard_pos = next_pos
  return visited_positions

le_visited_positions = get_visited_positions(le_initial_guard_pos, le_initial_direction, le_obstacles_positions, le_board_table)
print("Visited a total of ", len(le_visited_positions), " positions.", sep = "")
# print("List of visited positions :\n", le_visited_positions, sep = "")
# print("\nFinal map, with visited positions marked with an ", marked_char, " :", sep = "")
# print_map(le_board_table)

######
# PART 2
######

def check_if_loops(initial_guard_pos, initial_direction, obstacle_positions, board_table) :
  current_direction = initial_direction
  current_guard_pos = initial_guard_pos
  visited_positions = set()
  row_count = len(board_table)
  col_count = len(board_table[0])
  # then, move guard according to given rules, until it's out
  while 0 <= current_guard_pos[0] < row_count and 0 <= current_guard_pos[1] < col_count :
    # keep track of visited positions
    if (current_guard_pos, current_direction) not in visited_positions :
      visited_positions.add((current_guard_pos, current_direction))
      board_table[current_guard_pos[0]][current_guard_pos[1]] = marked_char
    else :
      return True
    next_pos = (current_guard_pos[0] + current_direction[0], current_guard_pos[1] + current_direction[1])
    if next_pos in obstacle_positions :
      current_direction = get_rotated_90(current_direction)
    else :
      current_guard_pos = next_pos
  # print_map(board_table) # [debugging]
  # print(visited_positions) # [debugging]
  return False

def get_visited_positions_with_directions (initial_guard_pos, initial_direction, obstacle_positions, board_table) :
  current_direction = initial_direction
  current_guard_pos = initial_guard_pos
  visited_positions = set()
  row_count = len(board_table)
  col_count = len(board_table[0])
  # then, move guard according to given rules, until it's out
  while 0 <= current_guard_pos[0] < row_count and 0 <= current_guard_pos[1] < col_count :
    # keep track of visited positions
    if (current_guard_pos, current_direction) not in visited_positions :
      visited_positions.add((current_guard_pos, current_direction))
      board_table[current_guard_pos[0]][current_guard_pos[1]] = marked_char
    else :
      break
    next_pos = (current_guard_pos[0] + current_direction[0], current_guard_pos[1] + current_direction[1])
    if next_pos in obstacle_positions :
      current_direction = get_rotated_90(current_direction)
    else :
      current_guard_pos = next_pos
  return visited_positions

def count_new_obstacle_candidates(initial_guard_pos, initial_direction, obstacle_positions, board_table) :
  obstacle_candidates_count = 0
  original_visited_positions = get_visited_positions(initial_guard_pos, initial_direction, obstacle_positions, board_table)
  for row_idx in range(le_row_count) :
    if (row_idx % 10 == 0) :
      print("Reached row_idx = ", row_idx, sep = "")
    for col_idx in range(le_col_count) :
      curr_cell = board_table[row_idx][col_idx]
      # if curr_cell != obstacle_char and curr_cell != guard_char and (row_idx, col_idx) not in obstacle_positions :
      if curr_cell != obstacle_char and curr_cell != guard_char and (row_idx, col_idx) in original_visited_positions :
        board_table[row_idx][col_idx] = candidate_obstacle_char
        obstacle_positions.add((row_idx, col_idx))
        if (check_if_loops(initial_guard_pos, initial_direction, obstacle_positions, board_table)) :
          obstacle_candidates_count += 1
        obstacle_positions.remove((row_idx, col_idx))
        board_table[row_idx][col_idx] = curr_cell
  return obstacle_candidates_count

le_obstacle_candidates_count = count_new_obstacle_candidates(le_initial_guard_pos, le_initial_direction, le_obstacles_positions, le_board_table)

print("Number of candidates found for a new obstacle that would make the guard get on a loop : ", \
  le_obstacle_candidates_count, sep = "")

# Alternative solution (unfinished)

# def count_new_obstacle_candidates_eff(initial_guard_pos, initial_direction, obstacle_positions, board_table) :
#   # [TBC]
#   row_count = len(board_table)
#   col_count = len(board_table[0])
#   obstacle_candidates_count = 0
#   original_visited_positions_with_direction = get_visited_positions_with_directions(initial_guard_pos, initial_direction, obstacle_positions, board_table)
#   # print("original_visited_positions_with_direction :\n", original_visited_positions_with_direction, sep = "") # [debugging]
#   for pos_with_dir in original_visited_positions_with_direction :
#     dir = pos_with_dir[1]
#     row_idx, col_idx = pos_with_dir[0][0] - dir[0], pos_with_dir[0][0] + - dir[1]
#     dir = get_rotated_90(dir)
#     while 0 <= row_idx < row_count and 0 <= col_idx < col_count:
#       if board_table[row_idx][col_idx] == obstacle_char :
#       pass
#     elif pos_with_dir[1] == (0, 1) :
#       pass
#     elif pos_with_dir[1] == (1, 0) :
#       pass
#     elif pos_with_dir[1] == (0, -1) :
#       pass
#     else :
#       raise Exception("count_new_obstacle_candidates_eff error : bad direction !")
#   return obstacle_candidates_count

# le_obstacle_candidates_count_eff = count_new_obstacle_candidates_eff(le_initial_guard_pos, le_initial_direction, le_obstacles_positions, le_board_table)
# print("Number of candidates found for a new obstacle that would make the guard get on a loop : ", \
#   le_obstacle_candidates_count_eff, sep = "")