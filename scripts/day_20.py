import helpers
import copy

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
def estimate_distance(maze, pos_1, pos_2) :
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
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(maze, start_pos, end_pos), "path" : [], "has_cheat" : False}
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
      neighbor_cost_estimate = neighbor_dist_start + estimate_distance(maze, neighbor_pos, end_pos)
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
def update_neighbors(maze, open_dict, closed_dict, chosen_pos, end_pos, with_cheats = False) :
  cheat_positions = (NO_POS, NO_POS)
  chosen_data = open_dict[chosen_pos]
  for neighbor_pos, dir, cost, is_cheat in get_neighbors(maze, chosen_pos, with_cheats) :
    if is_cheat :
      (pos_x, pos_y), (dir_x, dir_y) = neighbor_pos, dir
      cheat_positions = ((pos_x, pos_y), (pos_x + dir_x, pos_y + dir_y))
    if neighbor_pos in closed_dict :
      continue
    neighbor_dist_start = chosen_data["dist_start"] + cost
    neighbor_cost_estimate = neighbor_dist_start + estimate_distance(maze, neighbor_pos, end_pos)
    if neighbor_pos not in open_dict :
      open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
        , "path" : chosen_data["path"] + [(chosen_pos, dir)], "cheat_positions_set" : ((cheat_positions) | chosen_data["cheat_positions_set"])}
    elif open_dict[neighbor_pos]["cost_estimate"] > neighbor_cost_estimate :
      open_dict[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
        , "path" : chosen_data["path"] + [(chosen_pos, dir)], "cheat_positions_set" : ((cheat_positions) | chosen_data["cheat_positions_set"])}
  pass
#
# def explore_next_cell(maze, open_dict, closed_dict, end_pos) :
#   if len(open_dict) == 0 :
#     return
#   chosen_pos = find_pos_with_lowest_estimate(open_dict)
#   update_neighbors(maze, open_dict, closed_dict, chosen_pos, end_pos, False)
#   closed_dict[chosen_pos] = open_dict[chosen_pos]
#   open_dict.pop(chosen_pos)
#
def find_cheats_v2(maze) :
  start_pos, end_pos = find_start_and_end(maze)
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(maze, start_pos, end_pos), "path" : [], "has_cheat" : False}
  open_dict = {start_pos : start_data}
  closed_dict = dict()
  # first, explore without cheats
  while len(open_dict) > 0 and end_pos not in closed_dict :
    pos_with_lowest_est = find_pos_with_lowest_estimate(open_dict)
    update_neighbors(maze, open_dict, closed_dict, pos_with_lowest_est, end_pos, False)
    closed_dict[pos_with_lowest_est] = open_dict[pos_with_lowest_est]
    open_dict.pop(pos_with_lowest_est)
  least_cost_no_cheats = closed_dict[end_pos]["dist_start"]
  shortest_path_no_cheats = copy.deepcopy(closed_dict[end_pos]["path"])
  # Then try to cheat from each cell of the shortest path
  # [?]
  return dict()

helpers.LOG_DICT["T"][0] = True

helpers.print_log_entries("find_shortest_path(le_test_table)"\
  , find_shortest_path(le_test_table), log_cats = {"T"})

helpers.print_log_entries("find_shortest_path(le_char_table)"\
  , find_shortest_path(le_char_table), log_cats = {"T"})

le_test_cheats = find_cheats(le_test_table)

helpers.print_log_entries("find_cheats(le_test_table)"\
  , le_test_cheats, log_cats = {"T"})


le_good_cheats_count_test = 0
for cheat, val in le_test_cheats.items() :
  if val >= 1 :
    le_good_cheats_count_test += 1
helpers.print_log_entries("Good cheats count [test] : {}".format(le_good_cheats_count_test), log_cats={"R"})

le_cheats = find_cheats(le_char_table)

helpers.print_log_entries("find_cheats(le_char_table)"\
  , le_cheats, log_cats = {"T"})

le_good_cheats_count = 0
for cheat, val in le_cheats.items() :
  if val >= 100 :
    le_good_cheats_count += 1

helpers.print_log_entries("Good cheats count : {}".format(le_good_cheats_count), log_cats={"R"})

######
# PART 2
######