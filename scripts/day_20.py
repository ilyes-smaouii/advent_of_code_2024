import helpers
import copy
import time

# open file, collect content
le_filename = "../inputs/day_20_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
# le_lines = helpers.get_file_content_as_lines(le_filename)
le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_table = helpers.raw_to_table("""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""")

######
# PART 1
######

START_CHAR = "S"
END_CHAR = "E"
WALL_CHAR = "#"
EMPTY_CHAR = "."
DIRECTIONS = {
  (-1, 0), # up
  (+1, 0), # down
  (0, -1), # left
  (0, +1), # right
}
DIR_CHARS = {
  (-1, 0) : "^", # up
  (+1, 0) : "v", # down
  (0, -1) : "<", # left
  (0, +1) : ">", # right
}
STEP_COST = 1
NO_POS = (-1, -1)
NO_DIR = (0, 0)

def find_start_and_end(maze) :
  start_pos, end_pos = NO_POS, NO_POS
  for row_idx in range(len(maze)) :
    for col_idx in range(len(maze[0])) :
      if maze[row_idx][col_idx] == START_CHAR :
        start_pos = (row_idx, col_idx)
      if maze[row_idx][col_idx] == END_CHAR :
        end_pos = (row_idx, col_idx)
  if start_pos == NO_POS or end_pos == NO_POS :
    raise Exception("Error : didn't find start or end position !"\
      "\n(start_pos = {}, end_pos = {})".format(start_pos, end_pos))
  else :
    return start_pos, end_pos
#

def manhattan_distance(pos_1, pos_2) :
  pos_1_row, pos_1_col = pos_1
  pos_2_row, pos_2_col = pos_2
  return abs(pos_2_row - pos_1_row) + abs(pos_2_col - pos_1_col)

def estimate_distance(pos_1, pos_2) :
  return STEP_COST * manhattan_distance(pos_1, pos_2)
#

def get_neighbors(maze, pos, with_cheat = False) :
  pos_row, pos_col = pos
  row_count = len(maze)
  col_count = len(maze[0])
  neighbors_with_data = set()
  for dir_row, dir_col in DIRECTIONS :
    new_row, new_col = pos_row + dir_row, pos_col + dir_col
    if not (0 <= new_row <= row_count - 1 and 0 <= new_col <= col_count - 1) :
      continue 
    if 0 <= new_row < row_count and\
      0 <= new_col < col_count :
      if maze[new_row][new_col] != WALL_CHAR :
        neighbors_with_data.add(((new_row, new_col), (dir_row, dir_col), STEP_COST, False))
      elif with_cheat :
        neighbors_with_data.add(((new_row, new_col), (dir_row, dir_col), STEP_COST, True))
  helpers.print_log_entries("get_neighbors() - neighbors_with_data :", neighbors_with_data, log_cats = {"D"})
  return neighbors_with_data
#

def get_neighbor_wall_cells(maze, pos) :
  pos_row, pos_col = pos
  row_count = len(maze)
  col_count = len(maze[0])
  neighbors_with_data = set()
  for dir_row, dir_col in DIRECTIONS :
    new_row, new_col = pos_row + dir_row, pos_col + dir_col
    if not (0 <= new_row <= row_count - 1 and 0 <= new_col <= col_count - 1) :
      continue 
    if 0 <= new_row < row_count and\
      0 <= new_col < col_count :
      if maze[new_row][new_col] == WALL_CHAR :
        neighbors_with_data.add(((new_row, new_col), (dir_row, dir_col), STEP_COST, True))
  helpers.print_log_entries("get_neighbor_wall_cells() - neighbors_with_data :", neighbors_with_data, log_cats = {"D"})
  return neighbors_with_data
#
def is_accessible_pos(maze, pos) :
  row_count = len(maze)
  col_count = len(maze[0])
  pos_row, pos_col = pos
  if 0 <= pos_row <= row_count - 1 and 0 <= pos_col <= col_count - 1 :
    return maze[pos_row][pos_col] != WALL_CHAR
  return False
#
def find_pos_with_lowest_estimate(open_dict) :
  chosen_pos = next(iter(open_dict))
  curr_estimate = open_dict[chosen_pos]["cost_estimate"]
  for pos, data in open_dict.items() :
    if data["cost_estimate"] <= curr_estimate :
      chosen_pos = pos
      curr_estimate = data["cost_estimate"]
  return chosen_pos
#

def update_neighbor(open_dict, closed_dict, neighbor_pos, dir, cost, prev_pos, end_pos) :
  if neighbor_pos in closed_dict :
    helpers.print_log_entries("update_neighbor() - neighbor_pos {} already in closed_dict !".format(neighbor_pos), log_cats={"D"})
    return
  neighbor_dist_start = open_dict[prev_pos]["dist_start"] + cost
  neighbor_cost_estimate = neighbor_dist_start + estimate_distance(neighbor_pos, end_pos)
  if neighbor_pos not in open_dict :
    open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
      , "prev" : prev_pos}
  elif open_dict[neighbor_pos]["cost_estimate"] > neighbor_cost_estimate :
    open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
      , "prev" : prev_pos}
  pass
#

def finish_exploration(maze, end_pos, open_dict, closed_dict, max_cost = -1, explore_all = False) :
  while len(open_dict) > 0 and (explore_all or end_pos not in closed_dict) :
    pos_with_lowest_est = find_pos_with_lowest_estimate(open_dict)
    if open_dict[pos_with_lowest_est]["cost_estimate"] > max_cost > -1 :
      return
    for neighbor_pos, dir, cost, is_wall in get_neighbors(maze, pos_with_lowest_est, False) :
      update_neighbor(open_dict, closed_dict, neighbor_pos, dir, cost, pos_with_lowest_est, end_pos)
    closed_dict[pos_with_lowest_est] = open_dict.pop(pos_with_lowest_est)
  return
#
def find_cheatless_cost(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(start_pos, end_pos), "prev" : NO_POS}
  open_dict = {start_pos : start_data}
  closed_dict = dict()
  finish_exploration(maze, end_pos, open_dict, closed_dict, explore_all = False)
  return closed_dict[end_pos]["dist_start"]
#
def find_cheats_v3(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  end_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(start_pos, end_pos), "prev" : NO_POS}
  open_dict = {end_pos : end_data}
  closed_dict = dict()
  # first, explore map from end, to get minimum distance from each cell to the end
  finish_exploration(maze, start_pos, open_dict, closed_dict, explore_all = True)
  distance_to_end = dict()
  for row_idx in range(len(maze)) :
    for col_idx in range(len(maze[0])) :
      pos = row_idx, col_idx
      if pos in closed_dict :
        distance_to_end[pos] = closed_dict[pos]["dist_start"]
      elif pos in open_dict :
        distance_to_end[pos] = open_dict[pos]["dist_start"]
      elif not is_accessible_pos(maze, pos) :
        pass
      else :
        raise Exception("find_cheats_v3() error : pos {} should be in either closed_dict or open_dict !".format(pos))
  # compute "cheatless" path
  cheatless_path = [start_pos]
  next_pos = closed_dict[start_pos]["prev"]
  while next_pos != NO_POS :
    cheatless_path.append(next_pos)
    next_pos = closed_dict[next_pos]["prev"]
  cheatless_cost = len(cheatless_path) - 1
  # then, from each cell in cheatless path, try to go through neighboring walls, and compute distance to end using distance_to_end
  cheat_dict = dict()
  for tile_idx in range(len(cheatless_path)) :
    tile_pos = cheatless_path[tile_idx]
    tile_dist_start = tile_idx
    for neighbor_pos, dir, cost, is_wall in get_neighbor_wall_cells(maze, tile_pos) :
      (pos_row, pos_col), (dir_row, dir_col) = neighbor_pos, dir
      cheat_positions = ((pos_row, pos_col), (pos_row + dir_row, pos_col + dir_col))
      after_wall_pos = pos_row + dir_row, pos_col + dir_col
      if is_accessible_pos(maze, after_wall_pos) :
        after_wall_dist = tile_dist_start + 2 * cost
        cheat_cost = after_wall_dist + distance_to_end[after_wall_pos]
        cheat_dict[cheat_positions] = min(cheat_cost, cheatless_cost)
  return cheat_dict

# helpers.LOG_DICT["T"][0] = True
helpers.LOG_DICT["DICT_LEN"] = [False, "[DICT_LEN]"]
helpers.LOG_DICT["DIST"] = [True, "[DIST]"]

le_test_cheats_dict = find_cheats_v3(le_test_table)
helpers.print_log_entries(find_cheats_v3(le_test_table), log_cats={"T"})
le_cheatless_count = find_cheatless_cost(le_char_table)
le_cheats_dict = find_cheats_v3(le_char_table)
le_good_cheats_count = 0
for cost in le_cheats_dict.values() :
  if cost <= le_cheatless_count - 100 :
    le_good_cheats_count += 1

helpers.print_log_entries("Number of \"good\" cheats : {}".format(le_good_cheats_count), log_cats={"R"})

######
# PART 2
######

def find_cheats_up_to_20(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  end_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(start_pos, end_pos), "prev" : NO_POS}
  open_dict = {end_pos : end_data}
  closed_dict = dict()
  # first, explore map from end, to get minimum distance from each cell to the end
  finish_exploration(maze, start_pos, open_dict, closed_dict, explore_all = True)
  distance_to_end = dict()
  for row_idx in range(len(maze)) :
    for col_idx in range(len(maze[0])) :
      pos = row_idx, col_idx
      if pos in closed_dict :
        distance_to_end[pos] = closed_dict[pos]["dist_start"]
      elif pos in open_dict :
        distance_to_end[pos] = open_dict[pos]["dist_start"]
      elif not is_accessible_pos(maze, pos) :
        pass
      else :
        raise Exception("find_cheats_v3() error : pos {} should be in either closed_dict or open_dict !".format(pos))
  # compute "cheatless" path
  cheatless_path = [start_pos]
  next_pos = closed_dict[start_pos]["prev"]
  while next_pos != NO_POS :
    cheatless_path.append(next_pos)
    next_pos = closed_dict[next_pos]["prev"]
  cheatless_cost = len(cheatless_path) - 1
  # then, from each cell in cheatless path, try cheats of length 20 or under around, and check the new path length we get
  cheat_dict = dict()
  for tile_idx in range(len(cheatless_path)) :
    tile_pos = cheatless_path[tile_idx]
    (tile_pos_row, tile_pos_col) = tile_pos
    tile_dist_start = tile_idx
    for row_diff in range(-20, 20 + 1) :
      max_remaining_diff = 20 - abs(row_diff)
      for col_diff in range(-max_remaining_diff, max_remaining_diff + 1) :
        cheat_positions = (tile_pos, (tile_pos_row + row_diff, tile_pos_col + col_diff))
        after_cheat_pos = (tile_pos_row + row_diff, tile_pos_col + col_diff)
        if is_accessible_pos(maze, after_cheat_pos) :
          after_cheat_dist = tile_dist_start + abs(row_diff) + abs(col_diff)
          cheat_cost = min(cheatless_cost, after_cheat_dist + distance_to_end[after_cheat_pos])
          if cheat_positions in cheat_dict :
            cheat_dict[cheat_positions] = min(cheat_dict[cheat_positions], cheat_cost)
          else :
            cheat_dict[cheat_positions] = cheat_cost
  return cheat_dict

le_cheats_up_to_20_dict = find_cheats_up_to_20(le_char_table)
le_good_cheats_up_to_20_count = 0
for cost in le_cheats_up_to_20_dict.values() :
  if cost <= le_cheatless_count - 100 :
    le_good_cheats_up_to_20_count += 1

helpers.print_log_entries("Number of \"good\" cheats w/ up to 20 moves : {}".format(le_good_cheats_up_to_20_count), log_cats={"R"})