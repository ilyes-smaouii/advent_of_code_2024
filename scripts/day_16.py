import helpers
import copy

# open file, collect content
le_filename = "../inputs/day_16_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_table = helpers.raw_to_table("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""")
le_test_table_2 = helpers.raw_to_table("""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""")

######
# PART 1
######

# Node rep : ((x, y), (dir))
# dir rep : ?

WALL_CHAR = "#"
EMPTY_CHAR = "."
START_CHAR = "S"
END_CHAR = "E"
TRAVERSABLE_CELLS = (EMPTY_CHAR, START_CHAR, END_CHAR)
NO_POS = (-1, -1)
NO_DIR = (-1, -1)
NO_POS_NO_DIR = (NO_POS, NO_DIR)
START_DIR = (0, +1)
ALL_DIRECTIONS = set({
  (-1, 0),
  (+1, 0),
  (0, -1),
  (0, +1),
})
MOVE_COST = 1
TURN_COST = 1000
START_PREV = NO_POS
DIR_CHARS = {
  (-1, 0) : "^",
  (+1, 0) : "v",
  (0, -1) : "<",
  (0, +1) : ">",
}

# def get_nodes_set(char_table) :
#   nodes_set = set()
#   start_pos = NO_POS
#   for row_idx in range(len(char_table)) :
#     for col_idx in range(len(char_table)) :
#       curr_cell = char_table[row_idx][col_idx]
#       if curr_cell == WALL_CHAR :
#         continue
#       elif curr_cell == EMPTY_CHAR :
#         nodes_set.add(((row_idx, col_idx), (-1, 0)))
#         nodes_set.add(((row_idx, col_idx), (+1, 0)))
#         nodes_set.add(((row_idx, col_idx), (0, -1)))
#         nodes_set.add(((row_idx, col_idx), (0, +1)))
#       elif curr_cell
#   pass

def find_start_and_end(char_table) :
  """
  Find and return starting and ending positions
  Starting position is associated with a starting direction, unlike the Ending position
  """
  start_pos_dir = NO_POS_NO_DIR
  end_pos = NO_POS
  found_start = False
  found_end = False
  for row_idx in range(len(char_table)) :
    for col_idx in range(len(char_table[0])) :
      if char_table[row_idx][col_idx] == START_CHAR :
        start_pos_dir = ((row_idx, col_idx), START_DIR)
        found_start = True
      if char_table[row_idx][col_idx] == END_CHAR :
        end_pos = (row_idx, col_idx)
        found_end = True
      if found_start and found_end :
        # helpers.print_log_entries("start_pos_dir, end_pos :", "{}, {}".format(start_pos_dir, end_pos), log_cats = {"D"})
        return start_pos_dir, end_pos
  return start_pos_dir, end_pos

def count_turns(dir_1, dir_2) :
  dir_1_x, dir_1_y = dir_1
  dir_2_x, dir_2_y = dir_2
  if dir_1_x != 0 :
    if dir_2_y != 0 :
      return 1
    else :
      return abs(dir_1_x - dir_2_x)
  else :
    if dir_2_x != 0 :
      return 1
    else :
      return abs(dir_1_y - dir_2_y)

def estimate_remaining_cost_to_goal(pos_dir, end_pos) :
  pos_x, pos_y = pos_dir[0]
  dir_x, dir_y = pos_dir[1]
  end_pos_x, end_pos_y = end_pos
  # Use Manhattan distance as heuristic estimate
  final_cost = MOVE_COST * abs(pos_x - end_pos_x) + MOVE_COST * abs(pos_y - end_pos_y)
  # TO-DO : add cost of turning ?
  to_end_dir_x = end_pos_x - pos_x
  to_end_dir_y = end_pos_y - pos_y
  if to_end_dir_x != 0 :
    to_end_dir_x //= abs(to_end_dir_x)
  if to_end_dir_y != 0 :
    to_end_dir_y //= abs(to_end_dir_y)
  turn_cost = TURN_COST * count_turns((dir_x, dir_y), (to_end_dir_x, to_end_dir_y))
  # final_cost += turn_cost
  return final_cost

def get_neighbors(char_table, pos_dir) :
  """
  element format :
  (pos, dir, traversal_cost)
  """
  # helpers.print_log_entries("get_neighbors() - called with pos_dir = {}".format(pos_dir), log_cats = {"D", "ARGS"})
  final_neighbors = dict()
  (pos_x, pos_y), (dir_x, dir_y) = pos_dir
  next_pos_x, next_pos_y = pos_x + dir_x, pos_y + dir_y
  if char_table[next_pos_x][next_pos_y] in TRAVERSABLE_CELLS :
    # cost to move to neighbor in current direction
    final_neighbors[((next_pos_x, next_pos_y), (dir_x, dir_y))] = MOVE_COST
  turn_right = (+dir_y, -dir_x)
  turn_left = (-dir_y, +dir_x)
  turn_twice = (-dir_x, -dir_y)
  final_neighbors[((pos_x, pos_y), turn_right)] = TURN_COST
  final_neighbors[((pos_x, pos_y), turn_left)] = TURN_COST
  final_neighbors[((pos_x, pos_y), turn_twice)] = 2*TURN_COST + 13
  # final_neighbors[((pos_x, pos_y), (-dir_x, -dir_y))] = 2*TURN_COST
  # for new_dir in ALL_DIRECTIONS.difference((dir_x, dir_y)) :
  #   # cost to turn 
  #   final_neighbors[((pos_x, pos_y), new_dir)] = count_turns(new_dir, (dir_x, dir_y)) * TURN_COST
  return final_neighbors

def find_shortest_path_aux(char_table) :
  start_pos_dir, end_pos = find_start_and_end(char_table)
  # (pos_dir, cost_from_start, estimate_cost_to_goal, previous_cell)
  open_dict = {
    start_pos_dir : {"dist_start" : 0, "est_end" : estimate_remaining_cost_to_goal(start_pos_dir, end_pos), "prev" : []}
    }
  closed_dict = dict()
  end_reached = False
  # helpers.print_log_entries("open_dict : {}".format(open_dict), log_cats = {"D"})
  # helpers.print_log_entries("len(open_dict) : {}".format(len(open_dict)), log_cats = {"D"})
  while len(open_dict) > 0 and not end_reached :
    some_candidate_metadata = next(iter(open_dict.values()))
    # helpers.print_log_entries("some_candidate_metadata : {}".format(some_candidate_metadata), log_cats = {"D"})
    cost_estimate = some_candidate_metadata["dist_start"] + some_candidate_metadata["est_end"]
    chosen_candidate_pos_dir = None
    for candidate_pos_dir, candidate_metadata in open_dict.items() :
      if candidate_metadata["dist_start"] + candidate_metadata["est_end"] <= cost_estimate :
        cost_estimate = candidate_metadata["dist_start"] + candidate_metadata["est_end"]
        chosen_candidate_pos_dir = candidate_pos_dir
    # helpers.print_log_entries("find_shortest_path_aux() - chosen_candidate_pos_dir"\
    #   " : {}".format(chosen_candidate_pos_dir), log_cats = {"D"})
    # helpers.print_log_entries("find_shortest_path_aux() - cost_estimate"\
    #   " : {}".format(cost_estimate), log_cats = {"D"})
    if chosen_candidate_pos_dir[0] == end_pos :
      end_reached = True
      closed_dict[chosen_candidate_pos_dir] = open_dict[chosen_candidate_pos_dir]
      open_dict.pop(chosen_candidate_pos_dir)
    else :
      for neighbor_pos_dir, distance_to_neighbor in get_neighbors(char_table, chosen_candidate_pos_dir).items() :
        if neighbor_pos_dir in closed_dict :
          continue
        cost_to_neighbor = open_dict[chosen_candidate_pos_dir]["dist_start"] + distance_to_neighbor
        neighor_estimate_to_goal = estimate_remaining_cost_to_goal(neighbor_pos_dir, end_pos)
        if neighbor_pos_dir not in open_dict :
          open_dict[neighbor_pos_dir] = {"dist_start" : cost_to_neighbor, "est_end" : neighor_estimate_to_goal, \
            "prev" : open_dict[chosen_candidate_pos_dir]["prev"] + [chosen_candidate_pos_dir]}
        else :
          open_dict[neighbor_pos_dir]["dist_start"] = \
            min(open_dict[neighbor_pos_dir]["dist_start"], cost_to_neighbor)
      closed_dict[chosen_candidate_pos_dir] = open_dict[chosen_candidate_pos_dir]
      open_dict.pop(chosen_candidate_pos_dir)
    # helpers.print_log_entries("closed_dict.keys() : {}".format(closed_dict.keys()), log_cats = {"D"})
    # helpers.print_log_entries("closed_dict : {}".format(closed_dict), log_cats = {"D"})
  helpers.print_log_entries("len(closed_dict) : {}".format(len(closed_dict)), log_cats = {"D"})
  return closed_dict

def display_path(char_table, path) :
  table_copy = copy.deepcopy(char_table)
  for ((pos_x, pos_y), dir) in path :
    table_copy[pos_x][pos_y] = DIR_CHARS[dir]
  print(helpers.table_to_raw(table_copy))

def find_sortest_path(char_table) :
  start_pos, end_pos = find_start_and_end(char_table)
  closed_dict = find_shortest_path_aux(char_table)
  for pos_dir in closed_dict :
    if pos_dir[0] == end_pos :
      helpers.print_log_entries("path length : {}".format(len(closed_dict[pos_dir]["prev"])), log_cats = {"D"})
      le_path = closed_dict[pos_dir]["prev"]
      display_path(char_table, le_path)
      # helpers.print_log_entries("Path : {}".format(closed_dict[pos_dir]["prev"]), log_cats = {"FP"})
      path_str = "\n".join(str(elem) for elem in closed_dict[pos_dir]["prev"])
      helpers.print_log_entries("Path : {}".format(path_str), log_cats = {"FP"})
      return closed_dict[pos_dir]["dist_start"]

helpers.LOG_DICT["T"] = [True, "[TESTING]"]
helpers.LOG_DICT["D"] = [True, "[DEBUG]"]
helpers.LOG_DICT["FP"] = [False, "[FULL_PATH]"]

# helpers.print_log_entries(find_shortest_path_aux(le_char_table), log_cats = {"T"})
# for dir1 in ALL_DIRECTIONS :
#   for dir2 in ALL_DIRECTIONS :
#     helpers.print_log_entries("count_turns({}, {}) : {}".format(dir1, dir2, count_turns(dir1, dir2)), log_cats = {"T"})
#
# helpers.print_log_entries(find_sortest_path(le_test_table), log_cats = {"T"})
# helpers.print_log_entries(find_sortest_path(le_test_table_2), log_cats = {"T"})
# helpers.print_log_entries(find_sortest_path(le_char_table), log_cats = {"R"})

######
# PART 2
######

def find_shortest_paths_aux(char_table) :
  start_pos_dir, end_pos = find_start_and_end(char_table)
  # (pos_dir, cost_from_start, estimate_cost_to_goal, previous_cell)
  shortest_found = -1
  found_paths = []
  open_dict = {
    start_pos_dir : {"dist_start" : 0, "est_end" : estimate_remaining_cost_to_goal(start_pos_dir, end_pos), "prev" : set()}
    }
  closed_dict = dict()
  # helpers.print_log_entries("open_dict : {}".format(open_dict), log_cats = {"D"})
  # helpers.print_log_entries("len(open_dict) : {}".format(len(open_dict)), log_cats = {"D"})
  finished_exploration = False
  while len(open_dict) > 0 and not finished_exploration :
    # if ((9, 3), (-1, 0)) in closed_dict :
    #   helpers.print_log_entries("closed_dict[((9, 3), (-1, 0))] : {}".format(closed_dict[((9, 3), (-1, 0))]), log_cats = {"D"})
    if ((9, 3), (-1, 0)) in open_dict :
      helpers.print_log_entries("open_dict[((9, 3), (-1, 0))] : {}".format(open_dict[((9, 3), (-1, 0))]), log_cats = {"D"})
    some_candidate_metadata = next(iter(open_dict.values()))
    # helpers.print_log_entries("some_candidate_metadata : {}".format(some_candidate_metadata), log_cats = {"D"})
    cost_estimate = some_candidate_metadata["dist_start"] + some_candidate_metadata["est_end"]
    chosen_candidate_pos_dir = None
    for candidate_pos_dir, candidate_metadata in open_dict.items() :
      if candidate_metadata["dist_start"] + candidate_metadata["est_end"] <= cost_estimate :
        cost_estimate = candidate_metadata["dist_start"] + candidate_metadata["est_end"]
        chosen_candidate_pos_dir = candidate_pos_dir
    # helpers.print_log_entries("find_shortest_path_aux() - chosen_candidate_pos_dir"\
    #   " : {}".format(chosen_candidate_pos_dir), log_cats = {"D"})
    # helpers.print_log_entries("find_shortest_path_aux() - cost_estimate"\
    #   " : {}".format(cost_estimate), log_cats = {"D"})
    if chosen_candidate_pos_dir[0] == end_pos :
      closed_dict[chosen_candidate_pos_dir] = open_dict[chosen_candidate_pos_dir]
      if shortest_found == -1 or shortest_found >= open_dict[chosen_candidate_pos_dir]["dist_start"] :
        shortest_found = open_dict[chosen_candidate_pos_dir]["dist_start"]
        found_paths.append(open_dict[chosen_candidate_pos_dir]["prev"])
      elif shortest_found < open_dict[chosen_candidate_pos_dir]["dist_start"] :
        finished_exploration = True
      open_dict.pop(chosen_candidate_pos_dir)
    else :
      for neighbor_pos_dir, distance_to_neighbor in get_neighbors(char_table, chosen_candidate_pos_dir).items() :
        if neighbor_pos_dir in closed_dict :
          continue
        else :
          new_dist_start = open_dict[chosen_candidate_pos_dir]["dist_start"] + distance_to_neighbor
          neighor_estimate_to_goal = estimate_remaining_cost_to_goal(neighbor_pos_dir, end_pos)
          if neighbor_pos_dir not in open_dict :
            open_dict[neighbor_pos_dir] = {"dist_start" : new_dist_start, "est_end" : neighor_estimate_to_goal, \
              "prev" : open_dict[chosen_candidate_pos_dir]["prev"] | {chosen_candidate_pos_dir[0]}}
          else :
            old_dist_start = open_dict[neighbor_pos_dir]["dist_start"]
            if new_dist_start > old_dist_start :
              continue
            elif new_dist_start < old_dist_start :
              open_dict[neighbor_pos_dir]["dist_start"] = new_dist_start
              open_dict[neighbor_pos_dir]["prev"] = open_dict[chosen_candidate_pos_dir]["prev"] | {chosen_candidate_pos_dir[0]}
            else :
              open_dict[neighbor_pos_dir]["prev"] |= open_dict[chosen_candidate_pos_dir]["prev"] | {chosen_candidate_pos_dir[0]}
      closed_dict[chosen_candidate_pos_dir] = open_dict[chosen_candidate_pos_dir]
      open_dict.pop(chosen_candidate_pos_dir)
    # helpers.print_log_entries("closed_dict.keys() : {}".format(closed_dict.keys()), log_cats = {"D"})
  # helpers.print_log_entries("closed_dict : {}".format("\n".join(["{} : {}".format(k, ["{} : {}".format(v, closed_dict[k][v])\
  #   if v != "prev" else closed_dict[k][v][-3:] for v in closed_dict[k]]) for k in closed_dict])), log_cats = {"D"})
  if ((9, 3), (-1, 0)) in closed_dict :
    helpers.print_log_entries("closed_dict[((9, 3), (-1, 0))] : {}".format(closed_dict[((9, 3), (-1, 0))]), log_cats = {"D"})
  helpers.print_log_entries("len(closed_dict) : {}".format(len(closed_dict)), log_cats = {"D"})
  return closed_dict

def display_paths(char_table, paths) :
  table_copy = copy.deepcopy(char_table)
  for path in paths :
    for ((pos_x, pos_y), dir) in path :
      table_copy[pos_x][pos_y] = "O"
  print(helpers.table_to_raw(table_copy))

def display_tiles(char_table, tiles) :
  table_copy = copy.deepcopy(char_table)
  for (pos_x, pos_y) in tiles :
    table_copy[pos_x][pos_y] = "O"
  print(helpers.table_to_raw(table_copy))

def find_sortest_paths(char_table) :
  start_pos, end_pos = find_start_and_end(char_table)
  # shortest, found_paths = find_shortest_paths_aux(char_table)
  closed_dict = find_shortest_paths_aux(char_table)
  # print("Shortest : {}".format(shortest))
  # display_paths(char_table, found_paths)
  for pos_dir in closed_dict :
    if pos_dir[0] == end_pos :
      helpers.print_log_entries("path length : {}".format(len(closed_dict[pos_dir]["prev"])), log_cats = {"D"})
      display_tiles(char_table, closed_dict[pos_dir]["prev"])
      # helpers.print_log_entries("Path : {}".format(closed_dict[pos_dir]["prev"]), log_cats = {"FP"})
      path_str = "\n".join(str(elem) for elem in closed_dict[pos_dir]["prev"])
      helpers.print_log_entries("Path : {}".format(path_str), log_cats = {"FP"})
      helpers.print_log_entries("dist_start : {}".format(closed_dict[pos_dir]["dist_start"]), log_cats = {"R"})
      helpers.print_log_entries("Number of tiles : {}".format(len(closed_dict[pos_dir]["prev"])), log_cats = {"R"})
      return "good"
  # return "bad"

# def count_tiles_in_best_path(found_paths)

# helpers.print_log_entries(find_sortest_paths(le_test_table), log_cats = {"T"})
# helpers.print_log_entries(find_sortest_paths(le_test_table_2), log_cats = {"T"})
helpers.print_log_entries(find_sortest_paths(le_char_table), log_cats = {"R"})