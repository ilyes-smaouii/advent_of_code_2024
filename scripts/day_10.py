import helpers
import copy

# open file, collect content
le_filename = "../inputs/day_10_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = le_file_content.split("\n")
le_input_table = helpers.get_file_content_as_table(le_filename, lambda x : int(x) if ord('0') <= ord(x) <= ord('9') else -1)
# le_input_table = helpers.raw_to_table("""89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732""", int) # [testing]
# le_input_table = helpers.raw_to_table("""10..9..
# 2...8..
# 3...7..
# 4567654
# ...8..3
# ...9..2
# .....01""", lambda x : int(x) if x != "." else 20) # [testing]

######
# PART 1
######

helpers.LOG_DICT["D"]= (False, "[DEBUG]")
helpers.LOG_DICT["T"] = (False, "TESTING")
helpers.LOG_DICT["I"] = (False, "[INFO]")
helpers.LOG_DICT["TRAILS"] = (False, "[TRAIL_TRACKING]")
helpers.LOG_DICT["NEXT_CELLS"] = (False, "[NEXT_CELLS]")
helpers.LOG_DICT["CHECK_TRAILS"] = (False, "[CHECK_TRAILS]")
helpers.LOG_DICT["FROM_HT"] = (False, "[FROM_HT]")
# helpers.LOG_DICT["FINAL_TRAILS"] = (False, "[FINAL_TRAILS]")
helpers.LOG_DICT["TRAILHEADS"] = (False, "[TRAILHEADS]")
helpers.LOG_DICT["DIRECT"] = (False, "[DIRECT]")

# def find_trailheads(simple_table_view) :
#   trailheads = set()
#   for cell_pos, cell in helpers.SimpleTableViewCursor(simple_table_view) :
#     if True :
#       helpers.print_log_entries("find_trailheads() - cell_pos : " + str(cell_pos), log_cats = {"D"}) # [debugging]
#       helpers.print_log_entries("find_trailheads() - cell  : " + str(cell) + " of type " + str(type(cell))\
#         , log_cats = {"D"}) # [debugging]
#     if cell == 0 :
#       trailheads.add(cell_pos)
#   return trailheads

# le_simple_table = helpers.SimpleTableView(le_input_table)
# # le_simple_table = helpers.SimpleTableView([[1, 2, 0]])
# le_trailheads = find_trailheads(helpers.SimpleTableView(le_simple_table))
# helpers.print_log_entries("find_trailheads result :", str(le_trailheads), log_cats = {"T", "TRAILHEADS"}) # [testing]

# def get_neighboring_cells_set(simple_table_view, pos) :
#   helpers.print_log_entries("get_neighboring_cells_set() - got called with argument pos = " + str(pos), log_cats = {"D"})
#   neighboring_cells_set = set()
#   helpers.print_log_entries("get_neighboring_cells_set() - initializing by calling set_pos() with argument " + str(pos), log_cats = {"D"})
#   actual_new_pos, actual_new_cell = simple_table_view.set_pos(pos)
#   if actual_new_pos != pos :
#     raise Exception("get_neighboring_cells_set() error invalid position (expected " + str(pos) + ", got " + \
#       str(actual_new_pos) + ")")
#   st1 = helpers.SimpleTableView(simple_table_view, actual_new_pos)
#   st2 = helpers.SimpleTableView(simple_table_view, actual_new_pos)
#   st3 = helpers.SimpleTableView(simple_table_view, actual_new_pos)
#   st4 = helpers.SimpleTableView(simple_table_view, actual_new_pos)
#   st1.move_up()
#   st2.move_down()
#   st3.move_left()
#   st4.move_right()
#   helpers.print_log_entries("get_neighboring_cells_set() - will update with set :", \
#     str({st1.get_pos_and_cell(), st2.get_pos_and_cell(), st3.get_pos_and_cell(), st4.get_pos_and_cell()}), log_cats = {"NEXT_CELLS"})
#   neighboring_cells_set.update({st1.get_pos_and_cell(), st2.get_pos_and_cell(), st3.get_pos_and_cell(), st4.get_pos_and_cell()})
#   if (actual_new_pos, actual_new_cell) in neighboring_cells_set :
#     neighboring_cells_set.remove((actual_new_pos, actual_new_cell))
#   return neighboring_cells_set

# static_count = 0

# def explore_trails_from_trailhead(simple_table_view, trailhead_pos, curr_num = 0, curr_trail = []) :
#   global static_count
#   trailtails_set = set()
#   final_count = 0
#   curr_pos_and_cell = (trailhead_pos, simple_table_view.get_cell_at(trailhead_pos))
#   helpers.print_log_entries("explore_trails_from_trailhead() :", "trailhead_pos = " + str(trailhead_pos) + ", curr_trail = " + str(curr_trail), "\n", log_cats = {"TRAILS"})
#   if curr_pos_and_cell[1] == curr_num :
#     curr_trail = copy.deepcopy(curr_trail) + [curr_pos_and_cell]
#     if curr_num == 9 :
#       # print("found one", "curr_pos_and_cell = ", curr_pos_and_cell)
#       # print("returning (1, ", curr_pos_and_cell[0], ")", sep ="")
#       static_count += 1
#       helpers.print_log_entries("final_trail :", curr_trail, log_cats={"FINAL_TRAILS"})
#       return (1, {curr_pos_and_cell[0]})
#     else :
#       # helpers.print_log_entries("explore_trails_from_trailhead() - calling get_neighboring_cells_set() with argument "\
#       #                           "trailhead_pos = " + str(trailhead_pos), log_cats = {"D"})
#       neighboring_cells_set = get_neighboring_cells_set(simple_table_view, trailhead_pos)
#       helpers.print_log_entries("explore_trails_from_trailhead() - got neighboring_cells_set = " + str(neighboring_cells_set)\
#         , "from cell : " + str(curr_pos_and_cell), log_cats = {"NEXT_CELLS"})
#       for cell in neighboring_cells_set :
#         to_add = explore_trails_from_trailhead(simple_table_view, cell[0], curr_num + 1, curr_trail)
#         helpers.print_log_entries("found " + str(to_add) + " good trails for curr_num = "\
#           + str(curr_num), log_cats = {"CHECK_TRAILS"})
#         trailtails_set.update(to_add[1])
#         final_count += to_add[0]
#   else :
#     helpers.print_log_entries("cell not good for curr_num = " + str(curr_num) \
#       + ", cell_content =  " + str(curr_pos_and_cell[1]), "curr_trail = " + str(curr_trail), log_cats = {"TRAILS"})
#   return (len(trailtails_set), trailtails_set)

# def count_trails(simple_table_view, trailheads_positions) :
#   final_count = 0
#   for trailhead_pos in trailheads_positions :
#     explored = explore_trails_from_trailhead(simple_table_view, trailhead_pos)
#     helpers.print_log_entries("explored from : " + str(trailhead_pos), "to : " + str(explored), log_cats={"CHECK_TRAILS", "FROM_HT"})
#     final_count += explored[0]
#   return final_count

# helpers.print_log_entries("count_trails result : ", count_trails(le_simple_table, le_trailheads), log_cats = {"R"})
# helpers.print_log_entries("static_count result : ", static_count, log_cats = {"R"})

######
# PART 1 - More direct approach
######

def count_score_from_tailhead_aux(table, curr_pos, curr_distance = 0, curr_trail = []) :
  x, y = curr_pos
  tt_set = set()
  helpers.print_log_entries("count_score_from_tailhead_aux() - curr_trail : " + \
    str(curr_trail), log_cats = {"DIRECT"})
  row_count = len(table)
  col_count = len(table[0])
  curr_trail = curr_trail + [(table[x][y],curr_pos)]
  helpers.print_log_entries("count_score_from_tailhead_aux() - x, y, row_count, col_count :", \
    "{}, {}, {}, {}".format(x, y, col_count, row_count), log_cats = {"DIRECT"})
  if curr_pos == (-1, -1) :
    pass
  elif table[x][y] != curr_distance :
    pass
  elif curr_distance == 9 :
    tt_set = set({(x, y)})
  else :
    up_pos = (-1, -1)
    down_pos = (-1, -1)
    left_pos = (-1, -1)
    right_pos = (-1, -1)
    if x > 0 :
      up_pos = (x - 1, y)
    if x < row_count - 1 :
      down_pos = (x + 1, y)
    if y > 0 :
      left_pos = (x, y - 1)
    if y < col_count - 1 :
      right_pos = (x, y + 1)
    tt_set |= count_score_from_tailhead_aux(table, up_pos, curr_distance + 1, curr_trail)
    tt_set |= count_score_from_tailhead_aux(table, down_pos, curr_distance + 1, curr_trail)
    tt_set |= count_score_from_tailhead_aux(table, left_pos, curr_distance + 1, curr_trail)
    tt_set |= count_score_from_tailhead_aux(table, right_pos, curr_distance + 1, curr_trail)
  helpers.print_log_entries("count_score_from_tailhead_aux() - returning : " + str(tt_set), log_cats = {"DIRECT"})
  return tt_set

def count_score_from_tailhead(table, trailhead_pos) :
  return len(count_score_from_tailhead_aux(table, trailhead_pos, 0, []))

def count_scores_from_all_trailheads(table) :
  total_count = 0
  for row_idx in range(len(le_input_table)) :
    for col_idx in range(len(le_input_table[0])) :
      helpers.print_log_entries("Now counting for tailhead " + str((row_idx, col_idx)), log_cats = {"DIRECT"}) # [debugging]
      to_add = count_score_from_tailhead(table, (row_idx, col_idx))
      helpers.print_log_entries("Found " + str(to_add), log_cats = {"DIRECT"}) # [debugging]
      total_count += to_add
  return total_count

helpers.print_log_entries("Direct approach count : " + str(count_scores_from_all_trailheads(le_input_table)), log_cats={"R"})

######
# PART 2
######

helpers.LOG_DICT["PART2"] = (False, "[PART2]")

def count_trails_from_trailhead_aux(table, curr_pos, curr_distance = 0, curr_trail = []) :
  x, y = curr_pos
  tt_set = set()
  helpers.print_log_entries("count_score_from_tailhead_aux() - curr_trail : " + \
    str(curr_trail), log_cats = {"DIRECT"})
  row_count = len(table)
  col_count = len(table[0])
  curr_trail = curr_trail + [(table[x][y], curr_pos)]
  helpers.print_log_entries("count_score_from_tailhead_aux() - x, y, row_count, col_count :", \
    "{}, {}, {}, {}".format(x, y, col_count, row_count), log_cats = {"DIRECT"})
  if curr_pos == (-1, -1) :
    pass
  elif table[x][y] != curr_distance :
    pass
  elif curr_distance == 9 :
    tt_set = set({tuple(curr_trail)})
  else :
    up_pos = (-1, -1)
    down_pos = (-1, -1)
    left_pos = (-1, -1)
    right_pos = (-1, -1)
    if x > 0 :
      up_pos = (x - 1, y)
    if x < row_count - 1 :
      down_pos = (x + 1, y)
    if y > 0 :
      left_pos = (x, y - 1)
    if y < col_count - 1 :
      right_pos = (x, y + 1)
    tt_set |= count_trails_from_trailhead_aux(table, up_pos, curr_distance + 1, curr_trail)
    tt_set |= count_trails_from_trailhead_aux(table, down_pos, curr_distance + 1, curr_trail)
    tt_set |= count_trails_from_trailhead_aux(table, left_pos, curr_distance + 1, curr_trail)
    tt_set |= count_trails_from_trailhead_aux(table, right_pos, curr_distance + 1, curr_trail)
  helpers.print_log_entries("count_score_from_tailhead_aux() - returning : " + str(tt_set), log_cats = {"DIRECT", "PART2"})
  return tt_set

def count_trails_from_tailhead(table, trailhead_pos) :
  return len(count_trails_from_trailhead_aux(table, trailhead_pos, 0, []))

def count_trails_from_all_trailheads(table) :
  total_count = 0
  for row_idx in range(len(le_input_table)) :
    for col_idx in range(len(le_input_table[0])) :
      helpers.print_log_entries("Now counting for tailhead " + str((row_idx, col_idx)), log_cats = {"DIRECT"}) # [debugging]
      to_add = count_trails_from_tailhead(table, (row_idx, col_idx))
      helpers.print_log_entries("Found " + str(to_add), log_cats = {"DIRECT"}) # [debugging]
      total_count += to_add
  return total_count

helpers.print_log_entries("Direct approach count : " + str(count_trails_from_all_trailheads(le_input_table)), log_cats={"R"})