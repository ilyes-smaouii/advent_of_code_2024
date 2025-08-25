import helpers

# open file, collect content
le_filename = "../inputs/day_18_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)

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
STEP_COST = 1

def get_byte_positions(lines, byte_count = 1024) :
  byte_positions = set()
  for line in lines :
    col, row = line.split(",")
    byte_positions.add((int(row), int(col)))
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

def estimate_dist_to_end(maze, pos) :
  pos_row, pos_col = pos
  row_count = len(maze)
  col_count = len(maze[0])
  return STEP_COST * abs(row_count - 1 - pos_row) + STEP_COST * abs(col_count - 1 - pos_col)

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
        neighbors_with_cost.add(((new_row, new_col), STEP_COST))
  return neighbors_with_cost

def find_shortest_path(maze) :
  row_count = len(maze)
  col_count = len(maze[0])
  start_pos = (0, 0)
  end_pos = (row_count - 1, col_count - 1)
  start_data = {"dist_start" : 0, "cost_estimate" : 0 + estimate_dist_to_end(maze, start_pos), "path" : [start_pos]}
  open_set = {start_pos : start_data}
  closed_set = dict()
  while len(open_set) > 0 :
    chosen_pos = next(iter(open_set))
    curr_estimate = open_set[chosen_pos]["cost_estimate"]
    for pos, data in open_set.items() :
      if data["cost_estimate"] <= curr_estimate :
        chosen_pos = pos
        curr_estimate = data["cost_estimate"]
    for neighbor, cost in get_neighbors(maze, chosen_pos) :
      if neighbor in closed_set :
        continue
      neighbor_dist_start = open_set[chosen_pos]["dist_start"] + cost
      neighbor_cost_estimate = neighbor_dist_start + estimate_dist_to_end(maze, neighbor)
      if neighbor not in open_set :
        open_set[neighbor] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
          , "path" : open_set[chosen_pos]["path"] + [neighbor]}
      elif open_set[neighbor]["cost_estimate"] < neighbor_cost_estimate :
        open_set[neighbor] = {"dist_start" : neighbor_dist_start, "cost_estimate" : neighbor_cost_estimate\
          , "path" : open_set[chosen_pos]["path"] + [neighbor]}
  return closed_set[end_pos]["path"]
        

le_byte_positions = get_byte_positions(le_lines)
le_maze = get_maze(le_byte_positions)

######
# PART 2
######