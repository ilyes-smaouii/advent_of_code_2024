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

def estimate_distance(pos_1, pos_2) :
  pos_1_row, pos_1_col = pos_1
  pos_2_row, pos_2_col = pos_2
  return STEP_COST * abs(pos_2_row - pos_1_row) + STEP_COST * abs(pos_2_col - pos_1_col)
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

def get_neighbor_empty_cells(maze, pos) :
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
  helpers.print_log_entries("get_neighbor_empty_cells() - neighbors_with_data :", neighbors_with_data, log_cats = {"D"})
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

def find_shortest_path_aux(maze, start_pos, end_pos, cheat_seed = -1) :
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(start_pos, end_pos), "path" : [], "has_cheat" : False}
  open_set = {start_pos : start_data}
  closed_set = dict()
  # while len(open_set) > 0 and (end_pos not in closed_set):
  while len(open_set) > 0 :
    with_cheat = False
    chosen_pos = next(iter(open_set))
    chosen_data = open_set[chosen_pos]
    curr_estimate = open_set[chosen_pos]["cost_estimate"]
    for pos, data in open_set.items() :
      if data["cost_estimate"] <= curr_estimate :
        chosen_pos = pos
        chosen_data = data
        curr_estimate = data["cost_estimate"]
    if chosen_data["dist_start"] == cheat_seed :
      with_cheat = True
    for neighbor_pos, dir, cost, is_cheat in get_neighbors(maze, chosen_pos, with_cheat) :
      cheat_positions = (NO_POS, NO_POS)
      if is_cheat :
        pos_x, pos_y = neighbor_pos
        dir_x, dir_y = dir
        cheat_positions = ((pos_x, pos_y), (pos_x + dir_x, pos_y + dir_y))
      if neighbor_pos in closed_set :
        continue
      neighbor_dist_start = chosen_data["dist_start"] + cost
      neighbor_cost_estimate = neighbor_dist_start + estimate_distance(neighbor_pos, end_pos)
      if neighbor_pos not in open_set :
        open_set[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
          , "path" : chosen_data["path"] + [(chosen_pos, dir)], "has_cheat" : (is_cheat | chosen_data["has_cheat"])}
      elif open_set[neighbor_pos]["cost_estimate"] > neighbor_cost_estimate :
        open_set[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
          , "path" : chosen_data["path"] + [(chosen_pos, dir)], "has_cheat" : (is_cheat | chosen_data["has_cheat"])}
    closed_set[chosen_pos] = chosen_data
    open_set.pop(chosen_pos)
  path = closed_set[end_pos]["path"]
  path.append((end_pos, NO_DIR))
  for i in range(len(path)) :
    if closed_set[path[i][0]]["has_cheat"] :
      cheat_positions = (path[i][0], path[i+1][0])
      break
  return closed_set, cheat_positions
#

def find_shortest_path(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  closed_set, cheat_positions = find_shortest_path_aux(maze, start_pos, end_pos)
  return closed_set[end_pos]["dist_start"]
#

def find_cheats(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  no_cheat_shortest = find_shortest_path(maze)
  cheat_dict = dict()
  for i in range(no_cheat_shortest) :
    if i % 1 == 0 :
      print("Reached iteration n°{}".format(i))
    closed_set, cheat_positions = find_shortest_path_aux(maze, start_pos, end_pos, i)
    end_data = closed_set[end_pos]
    if end_data["has_cheat"] :
      if cheat_positions in cheat_dict :
        cheat_dict[cheat_positions] = min(cheat_dict[cheat_positions], end_data["dist_start"])
      else :
        cheat_dict[cheat_positions] = end_data["dist_start"]
  return cheat_dict
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
  # [path_prev]
  #   open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
  #     , "path" : open_dict[prev_pos]["path"] + [(prev_pos, dir)]}
  # elif open_dict[neighbor_pos]["cost_estimate"] > neighbor_cost_estimate :
  #   open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
  #     , "path" : open_dict[prev_pos]["path"] + [(prev_pos, dir)]}
    open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
      , "prev" : prev_pos}
  elif open_dict[neighbor_pos]["cost_estimate"] > neighbor_cost_estimate :
    open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
      , "prev" : prev_pos}
  pass
#

def finish_exploration(maze, end_pos, open_dict, closed_dict, max_cost = -1) :
  while len(open_dict) > 0 and end_pos not in closed_dict :
    pos_with_lowest_est = find_pos_with_lowest_estimate(open_dict)
    if open_dict[pos_with_lowest_est]["cost_estimate"] > max_cost > -1 :
      return
    for neighbor_pos, dir, cost, is_wall in get_neighbors(maze, pos_with_lowest_est, False) :
      update_neighbor(open_dict, closed_dict, neighbor_pos, dir, cost, pos_with_lowest_est, end_pos)
    closed_dict[pos_with_lowest_est] = open_dict.pop(pos_with_lowest_est)
  return
#
def finish_exploration_with_hint_minimal(maze, end_pos, open_dict, closed_dict, hint_closed, max_cost = -1) :
  while len(open_dict) > 0 and end_pos not in closed_dict :
    pos_with_lowest_est = find_pos_with_lowest_estimate(open_dict)
    if pos_with_lowest_est in hint_closed :
      diff = hint_closed[pos_with_lowest_est]["dist_start"] - open_dict[pos_with_lowest_est]["dist_start"]
      if diff > 0 :
        closed_dict[end_pos] = hint_closed[end_pos]
        closed_dict[end_pos]["dist_start"] -= diff
        return
    if open_dict[pos_with_lowest_est]["cost_estimate"] > max_cost > -1 :
      return
    for neighbor_pos, dir, cost, is_wall in get_neighbors(maze, pos_with_lowest_est, False) :
      update_neighbor(open_dict, closed_dict, neighbor_pos, dir, cost, pos_with_lowest_est, end_pos)
    closed_dict[pos_with_lowest_est] = open_dict.pop(pos_with_lowest_est)
  return
#
def find_cheats_v2(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  # [path_prev]
  # start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(start_pos, end_pos), "path" : []}
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(start_pos, end_pos), "prev" : NO_POS}
  open_dict = {start_pos : start_data}
  closed_dict = dict()
  # first, explore without cheats
  finish_exploration(maze, end_pos, open_dict, closed_dict)
  least_cost_no_cheats = closed_dict[end_pos]["dist_start"]
  # [path_prev]
  # shortest_path_no_cheats = copy.deepcopy(closed_dict[end_pos]["path"])
  shortest_path_no_cheats = []
  prev_pos = closed_dict[end_pos]["prev"]
  while prev_pos != NO_POS :
    shortest_path_no_cheats = [prev_pos] + shortest_path_no_cheats
    prev_pos = closed_dict[prev_pos]["prev"]
  # Then try to cheat from each cell of the shortest path
  # [?]
  # - cheat_dict = dict()
  # - for each i in [1, least_cost_no_cheats] :
  #   - bring remove last i elements from closed (excluding end_pos !), and add them to open
  #   - [alt 1] find moves through walls from -i-th element in path
  #   - [alt 1] for each move :
  #     - [alt 1] make copies of dicts
  #     - [alt 1] add to open
  #     - [alt 1] continue running, take note of final cost
  #   - [alt 2] update neighbors with cheats
  #   - [alt 2] for each wall cell/move through wall :
  #     - [alt 2] make copies of dicts
  #     - [alt 2] add to open
  #     - [alt 2] continue running from there, take note of final
  cheats_dict = dict()
  count = 0
  closed_dict_copy = copy.deepcopy(closed_dict)
  closed_dict.pop(end_pos)
  last_time = time.time()
  for i in range(least_cost_no_cheats) :
    if i % 5 == 0 :
      curr_time = time.time()
      helpers.print_log_entries("Reached iteration n°{} ({} since last_time)".format(i, curr_time - last_time), log_cats = {"ITER"})
      last_time = curr_time
    helpers.print_log_entries("len(closed_dict) : {}".format(len(closed_dict)), log_cats={"DICT_LEN"})
    helpers.print_log_entries("len(open_dict) : {}".format(len(open_dict)), log_cats={"DICT_LEN"})
    i_th_from_end = shortest_path_no_cheats[-i]
    open_dict[i_th_from_end] = closed_dict[i_th_from_end]
    closed_dict.pop(i_th_from_end)
    for neighbor_pos, dir, cost, is_wall in get_neighbor_wall_cells(maze, i_th_from_end) :
      if not is_wall :
        raise Exception("find_cheats_v2() error : get_neighbor_wall_cells() should only return wall cells !")
      temp_closed_dict = copy.copy(closed_dict)
      temp_open_dict = copy.copy(open_dict)
      update_neighbor(temp_open_dict, temp_closed_dict, neighbor_pos, dir, cost, i_th_from_end, end_pos)
      # finish_exploration(maze, end_pos, temp_open_dict, temp_closed_dict, least_cost_no_cheats)
      finish_exploration_with_hint_minimal(maze, end_pos, temp_open_dict, temp_closed_dict, closed_dict_copy, least_cost_no_cheats)
      if end_pos in temp_closed_dict :
        temp_cost = temp_closed_dict[end_pos]["dist_start"]
        if temp_cost <= least_cost_no_cheats - 100 :
          count += 1
          # (pos_x, pos_y), (dir_x, dir_y) = neighbor_pos, dir
          # cheats_dict[((pos_x, pos_y), (pos_x + dir_x, pos_y + dir_y))] = temp_cost
  return (cheats_dict, count)

# helpers.LOG_DICT["T"][0] = True
helpers.LOG_DICT["DICT_LEN"] = [False, "[DICT_LEN]"]
helpers.LOG_DICT["ITER"] = [True, "[ITER]"]

# helpers.print_log_entries("find_shortest_path(le_test_table)"\
# # , find_shortest_path(le_test_table), log_cats = {"T"})

# helpers.print_log_entries("find_shortest_path(le_char_table)"\
# # , find_shortest_path(le_char_table), log_cats = {"T"})

# le_test_cheats = find_cheats(le_test_table)

# helpers.print_log_entries("find_cheats(le_test_table)"\
# # , le_test_cheats, log_cats = {"T"})


# le_good_cheats_count_test = 0
# for cheat, val in le_test_cheats.items() :
#   if val >= 1 :
#     le_good_cheats_count_test += 1
# helpers.print_log_entries("Good cheats count [test] : {}".format(le_good_cheats_count_test), log_cats={"R"})

# le_cheats = find_cheats(le_char_table)

# helpers.print_log_entries("find_cheats(le_char_table)"\
# # , le_cheats, log_cats = {"T"})

# le_good_cheats_count = 0
# for cheat, val in le_cheats.items() :
#   if val >= 100 :
#     le_good_cheats_count += 1

# helpers.print_log_entries("Good cheats count : {}".format(le_good_cheats_count), log_cats={"R"})

print(find_cheats_v2(le_test_table))
le_cheats_dict, le_cheats_count = find_cheats_v2(le_char_table)

######
# PART 2
######