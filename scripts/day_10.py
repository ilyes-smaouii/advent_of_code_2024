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