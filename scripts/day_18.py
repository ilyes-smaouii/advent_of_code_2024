import helpers
import copy

# open file, collect content
le_filename = "../inputs/day_18_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_lines = helpers.raw_to_lines("""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""")

######
# PART 1
######

# 1 - Parse lines
# 2 - add walls
# 3 - A-star on resulting maze
# 4 - ?
# 5 - Profit

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
NO_DIR = (0, 0)

def get_byte_positions(lines, byte_count = 1024) :
  byte_positions = []
  for i in range(0, min(len(lines), byte_count)) :
    line = lines[i]
    col, row = line.split(",")
    byte_positions.append((int(row), int(col)))
  return byte_positions

def get_maze(byte_positions, row_count = 71, col_count = 71) :
  final_maze = []
  for row_idx in range(row_count) :
    final_maze.append([])
    for col_idx in range(col_count) :
      if (row_idx, col_idx) in byte_positions :
        final_maze[row_idx].append(WALL_CHAR)
      else :
        final_maze[row_idx].append(EMPTY_CHAR)
  return final_maze

def estimate_distance(maze, pos_1, pos_2) :
  pos_1_row, pos_1_col = pos_1
  pos_2_row, pos_2_col = pos_2
  return STEP_COST * abs(pos_2_row - pos_1_row) + STEP_COST * abs(pos_2_col - pos_1_col)

def get_neighbors(maze, pos) :
  pos_row, pos_col = pos
  row_count = len(maze)
  col_count = len(maze[0])
  neighbors_with_cost = set()
  for dir_row, dir_col in DIRECTIONS :
    new_row, new_col = pos_row + dir_row, pos_col + dir_col
    if 0 <= new_row < row_count and\
      0 <= new_col < col_count :
      if maze[new_row][new_col] != WALL_CHAR :
        neighbors_with_cost.add(((new_row, new_col), (dir_row, dir_col), STEP_COST))
  helpers.print_log_entries("neighbors_with_cost :", neighbors_with_cost, log_cats = {"D"})
  return neighbors_with_cost

def find_shortest_path_aux(maze) :
  row_count = len(maze)
  col_count = len(maze[0])
  start_pos = (0, 0)
  end_pos = (row_count - 1, col_count - 1)
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_distance(maze, start_pos, end_pos), "path" : []}
  open_set = {start_pos : start_data}
  closed_set = dict()
  while len(open_set) > 0 :
    chosen_pos = next(iter(open_set))
    chosen_data = open_set[chosen_pos]
    curr_estimate = open_set[chosen_pos]["cost_estimate"]
    for pos, data in open_set.items() :
      if data["cost_estimate"] <= curr_estimate :
        chosen_pos = pos
        chosen_data = data
        curr_estimate = data["cost_estimate"]
    for neighbor_pos, dir, cost in get_neighbors(maze, chosen_pos) :
      if neighbor_pos in closed_set :
        continue
      neighbor_dist_start = chosen_data["dist_start"] + cost
      neighbor_cost_estimate = neighbor_dist_start + estimate_distance(maze, neighbor_pos, end_pos)
      if neighbor_pos not in open_set :
        open_set[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
          , "path" : chosen_data["path"] + [(chosen_pos, dir)]}
      elif open_set[neighbor_pos]["cost_estimate"] > neighbor_cost_estimate :
        open_set[neighbor_pos] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
          , "path" : chosen_data["path"] + [(chosen_pos, dir)]}
    closed_set[chosen_pos] = chosen_data
    open_set.pop(chosen_pos)
  return closed_set
#
def find_shortest_path(maze) :
  row_count = len(maze)
  col_count = len(maze[0])
  closed = find_shortest_path_aux(maze)
  return closed[(row_count - 1, col_count - 1)]["path"]

def highlight_path(maze, path) :
  maze_copy = copy.deepcopy(maze)
  for (tile_row, tile_col), dir in path[:] :
    maze_copy[tile_row][tile_col] = DIR_CHARS[dir]
    # maze_copy[tile_row][tile_col] = "o"
  return maze_copy

le_test_byte_positions_list = get_byte_positions(le_test_lines, 12)
le_test_maze = get_maze(set(le_test_byte_positions_list), 7, 7)
le_test_shortest_path = find_shortest_path(le_test_maze)
le_test_highlighted_maze = highlight_path(le_test_maze, le_test_shortest_path)

le_byte_positions = get_byte_positions(le_lines, 1024)
le_maze = get_maze(set(le_byte_positions))
le_shortest_path = find_shortest_path(le_maze)
le_highlighted_maze = highlight_path(le_maze, le_shortest_path)


helpers.LOG_DICT["D"] = [False, "[DEBUG]"]
helpers.LOG_DICT["T"] = [False, "[TESTING]"]

helpers.print_log_entries("\n" + helpers.table_to_raw(le_test_maze), log_cats = "T")
helpers.print_log_entries("\n" + helpers.table_to_raw(le_test_highlighted_maze), log_cats = "T")
helpers.print_log_entries("len(le_test_shortest_path) :",\
  "{}".format(len(le_test_shortest_path)), log_cats = {"I"})

helpers.print_log_entries("len(le_shortest_path) :",\
  "{}".format(len(le_shortest_path)), log_cats = {"R"})

######
# PART 2
######

def find_cutting_off_byte_idx(byte_positions, row_count = 71, col_count = 71) :
  end_pos = (row_count - 1, col_count - 1)
  for i in range(len(byte_positions)) :
    if i % 50 == 0 :
      helpers.print_log_entries("Reached iteration n°{}".format(i), log_cats = {"I"})
    maze = get_maze(set(byte_positions[:i]), row_count, col_count)
    closed = find_shortest_path_aux(maze)
    if end_pos not in closed :
      return i
  return -1

def find_cutting_off_byte_idx_efficient(byte_positions, row_count = 71, col_count = 71) :
  end_pos = (row_count - 1, col_count - 1)
  max_i = len(byte_positions)
  temp_min = 0
  temp_max = max_i
  while temp_max > temp_min + 1 :
    helpers.print_log_entries("temp_max, temp_min : {}, {}".format(temp_max, temp_min), log_cats = {"D"})
    mid = (temp_max + temp_min) // 2
    maze = get_maze(set(byte_positions[:mid + 1]), row_count, col_count)
    closed = find_shortest_path_aux(maze)
    if end_pos not in closed :
      temp_max = mid
    else :
      temp_min = mid
  return temp_max

def find_cutting_off_byte_efficient(byte_positions) :
  byte_pos_idx = find_cutting_off_byte_idx_efficient(byte_positions)
  return byte_positions[byte_pos_idx]

le_full_byte_positions = get_byte_positions(le_lines, len(le_lines))

helpers.print_log_entries("find_cutting_off_byte_idx_efficient(le_full_byte_positions) :",\
  find_cutting_off_byte_idx_efficient(le_full_byte_positions), log_cats = {"R"})
cutoff_byte = find_cutting_off_byte_efficient(le_full_byte_positions)
helpers.print_log_entries("find_cutting_off_byte_efficient(le_full_byte_positions) :",\
  cutoff_byte, log_cats = {"R"})

helpers.print_log_entries("result with proper format :",\
  "{},{}".format(cutoff_byte[1], cutoff_byte[0]), log_cats = {"R"})