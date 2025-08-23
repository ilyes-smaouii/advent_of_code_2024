import helpers

# open file, collect content
le_filename = "../inputs/day_XX_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
le_char_table = helpers.get_file_content_as_table(le_filename)

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
        return start_pos_dir, end_pos
  return start_pos_dir, end_pos

def estimate_remaining_cost_to_goal(start_pos_dir, end_pos) :
  start_pos_x, start_pos_y = start_pos_dir[0]
  start_dir_x, start_dir_y = start_pos_dir[1]
  end_pos_x, end_pos_y = end_pos
  # Use Manhattan distance as heuristic estimate
  final_cost = MOVE_COST * abs(start_pos_x - end_pos_x) + MOVE_COST * abs(start_pos_y - end_pos_y)
  # TO-DO : add cost of turning ?
  diff_x = end_pos_x - start_pos_x
  diff_y = end_pos_y - start_pos_y
  turn_count = 0
  if diff_x != 0 :
    turn_count += 1
  if diff_y != 0 :
    turn_count += 1
  if start_dir_x * diff_x + start_dir_y * diff_y > 0 :
    turn_count -= 1
  final_cost += turn_count * TURN_COST
  return final_cost

def get_neighbors(char_table, pos_dir) :
  """
  element format :
  (pos, dir, traversal_cost)
  """
  final_neighbors = dict()
  (pos_x, pos_y), (dir_x, dir_y) = pos_dir
  next_pos_x, next_pos_y = pos_x + dir_x, pos_y + dir_y
  if char_table[next_pos_x][next_pos_y] in TRAVERSABLE_CELLS :
    # cost to move to neighbor in current direction
    final_neighbors[((next_pos_x, next_pos_y), (dir_x, dir_y))] = MOVE_COST
  for dir in ALL_DIRECTIONS.difference((dir_x, dir_y)) :
    # cost to turn 
    final_neighbors[((pos_x, pos_y), dir)] = TURN_COST
  return final_neighbors

def find_shortest_path_aux(char_table) :
  start_pos_dir, end_pos = find_start_and_end(char_table)
  # (pos_dir, cost_from_start, estimate_cost_to_goal, previous_cell)
  open_dict = {
    start_pos_dir : (0, estimate_remaining_cost_to_goal(start_pos_dir, end_pos), START_PREV)
    }
  closed_dict = dict()
  end_reached = True
  while len(open_dict) > 0 and not end_reached :
    some_candidate = open_dict.values()[0]
    cost_estimate = some_candidate[0] + some_candidate[1]
    chosen_candidate_pos_dir = None
    for candidate_pos_dir, candidate_metadata in open_dict :
      if candidate_metadata[0] + candidate_metadata[1] < cost_estimate :
        chosen_candidate_pos_dir = candidate_pos_dir
    if chosen_candidate_pos_dir[0] == end_pos :
      end_reached = True
      closed_dict[chosen_candidate_pos_dir] = open_dict[chosen_candidate_pos_dir]
      open_dict.pop(chosen_candidate_pos_dir)
    else :
      for neighbor_pos_dir, cost_to_neighbor in get_neighbors(char_table, chosen_candidate_pos_dir).items() :
        open_dict[neighbor_pos_dir] = (open_dict[chosen_candidate_pos_dir][0] + cost_to_neighbor,\
          estimate_remaining_cost_to_goal(neighbor_pos_dir, end_pos), chosen_candidate_pos_dir)
      closed_dict[chosen_candidate_pos_dir] = open_dict[chosen_candidate_pos_dir]
      open_dict.pop(chosen_candidate_pos_dir)
  return closed_dict

# def find_sortest_path(char_table) :
#   closed_dict = find_shortest_path_aux(char_table)

######
# PART 2
######