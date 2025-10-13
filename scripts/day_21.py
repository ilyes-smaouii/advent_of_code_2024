import helpers
import re
import copy

# open file, collect content
le_filename = "../inputs/day_21_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_lines = helpers.raw_to_lines("""029A
980A
179A
456A
379A""")

######
# PART 1
######

NO_DIR = (0, 0)
NO_POS = (-1, -1)
ALL_DIRS = {
  "^" : (-1, 0),
  "v" : (+1, 0),
  "<" : (0, -1),
  ">" : (0, +1),
}
# ALL_DIRS_REV = {
#   (-1, 0) : "^",
#   (+1, 0) : "v",
#   (0, -1) : "<",
#   (0, +1) : ">",
# }
BUTTON_POSITIONS_NUM_KEYPAD = {
  "7" : (0, 0),
  "8" : (0, 1),
  "9" : (0, 2),
  "4" : (1, 0),
  "5" : (1, 1),
  "6" : (1, 2),
  "1" : (2, 0),
  "2" : (2, 1),
  "3" : (2, 2),
  "G" : (3, 0),
  "0" : (3, 1),
  "A" : (3, 2),
}
BUTTON_POSITIONS_DIR_KEYPAD = {
  "G" : (0, 0),
  "^" : (0, 1),
  "A" : (0, 2),
  "<" : (1, 0),
  "v" : (1, 1),
  ">" : (1, 2),
}
PRESS_CHAR = "A"
GAP_CHAR = "G"

def compute_moves_pos (a_pos, b_pos) :
  """
  Computes moves to go from point A to point B
  """
  (a_row, a_col), (b_row, b_col) = a_pos, b_pos
  moves = dict()
  diff_x, diff_y = b_row - a_row, b_col - a_col
  if diff_x > 0 :
    moves["v"] = +diff_x
  elif diff_x < 0 :
    moves["^"] = -diff_x
  if diff_y > 0 :
    moves[">"] = +diff_y
  elif diff_y < 0 :
    moves["<"] = -diff_y
  return moves

def compute_moves_names (a_name, b_name, pos_dict) :
  a_pos = pos_dict[a_name]
  b_pos = pos_dict[b_name]
  return compute_moves_pos(a_pos, b_pos)

# def process_code_aux (code_str, pos_dict, prev_char = PRESS_CHAR) :
#   """
#   Process code to find resulting code/moves, i.e. that, when put into a robot on a keypad
#   will make it "type out" code_str
#   """
#   res_code_str = ""
#   for char_idx in range(len(code_str)) :
#     curr_char = code_str[char_idx]
#     # first, get number of each move needed to get from prev_char to curr_char
#     next_moves_dict = compute_moves_names(prev_char, curr_char, pos_dict)
#     # we should get two types of moves at most, and it seems intuitive to me all the corresponding
#     # moves should be grouped by move type, e.g. up-up-down-down, as opposed to up-down-up-down
#     # assuming I'm right, the question remains : how to order these two groups ?
#     # e.g. up-up-down-down or down-down-up-up ?
#     # Will try a random order first, and hope that doesn't have an impact on the result
#     # Update : looks like it doesn't have an impact after all, as long as the moves are grouped by
#     # same move type (?)
#     # Update : nvm it does actually, or at least it looks like it does
#     #
#     for move_type, move_count in next_moves_dict.items() :
#       res_code_str += move_count * move_type
#     res_code_str += PRESS_CHAR
#     prev_char = curr_char
#   return res_code_str
#
def get_orderings_aux(col_list) :
  if len(col_list) == 0 :
    return [""]
  res_set = []
  for i in range(len(col_list)) :
    for sub_ordering in get_orderings_aux(col_list[:i] + col_list[i+1:]) :
      res_set.append(col_list[i] + sub_ordering)
  # helpers.print_log_entries("get_orderings_aux() - returning...", log_cats={"D"})
  return res_set

def get_orderings(some_collection) :
  """
  Returns list of all possible ways to order characters in some_collection
  """
  list_of_orderings = get_orderings_aux(list(some_collection))
  return list_of_orderings
  # return set(list_of_orderings)

# [alt 2]
# def get_orderings_aux(col_set) :
#   if len(col_set) == 0 :
#     return [""]
#   res_set = []
#   for e in col_set :
#     for sub_ordering in get_orderings_aux(col_set.difference({e})) :
#       res_set.append(e + sub_ordering)
#   # helpers.print_log_entries("get_orderings_aux() - returning...", log_cats={"D"})
#   return res_set

# def get_orderings(collection) :
#   list_of_orderings = get_orderings_aux(set(collection))
#   return list_of_orderings
#   # return {list_of_orderings}

def remove_if_starts_with(coll, charset) :
  coll_copy = set()
  for e in coll :
    if e[0] not in charset :
      coll_copy.add(e)
  return coll_copy

def remove_if_ends_with(coll, charset) :
  coll_copy = set()
  for e in coll :
    if len(e) > 0 :
      if e[-1] not in charset :
        coll_copy.add(e)
    else :
      # ?
      pass
  return coll_copy
#
def process_code_aux_v2 (code_str, pos_dict, prev_char = PRESS_CHAR) :
  """
  Process code to find resulting code/moves, i.e. that, when put into a robot on a keypad
  will make it "type out" code_str
  """
  prev_pos = pos_dict[prev_char]
  prev_row, prev_col = prev_pos
  res_codes_temp = set()
  g_row, g_col = NO_POS
  if GAP_CHAR in pos_dict :
    g_row, g_col = pos_dict[GAP_CHAR]
  if len(code_str) > 0 :
    curr_char = code_str[0]
    curr_pos = pos_dict[curr_char]
    curr_row, curr_col = curr_pos
    next_moves_dict = dict()
    _orderings = set()
    next_moves_dict = compute_moves_pos(prev_pos, curr_pos)
    _orderings = get_orderings(next_moves_dict)
    # remove orderings that would make robot go over gap
    if prev_row == g_row and curr_col == g_col :
      _orderings = remove_if_starts_with(_orderings, set("><"))
      pass
    elif prev_col == g_col and curr_row == g_row :
      _orderings = remove_if_starts_with(_orderings, set("^v"))
      pass
    for ordering in _orderings :
      res_codes_temp.add("".join([move * next_moves_dict[move] for move in ordering]) + PRESS_CHAR)
    res_codes = set()
    for tmp_code_head in res_codes_temp :
      for tmp_code_rest in process_code_aux_v2(code_str[1:], pos_dict, curr_char) :
        res_codes.add(tmp_code_head + tmp_code_rest)
    return keep_shortest_ones(res_codes)
  else :
    return {""}

# def process_code (num_keypad_input) :
#   helpers.print_log_entries("num_keypad_input :", num_keypad_input, log_cats={"STEPS"})
#   first_dir_keypad_input = process_code_aux(num_keypad_input, BUTTON_POSITIONS_NUM_KEYPAD)
#   helpers.print_log_entries("first_dir_keypad_input :", first_dir_keypad_input, log_cats={"STEPS"})
#   second_dir_keypad_input = process_code_aux(first_dir_keypad_input, BUTTON_POSITIONS_DIR_KEYPAD)
#   helpers.print_log_entries("second_dir_keypad_input :", second_dir_keypad_input, log_cats={"STEPS"})
#   third_dir_keypad_input = process_code_aux(second_dir_keypad_input, BUTTON_POSITIONS_DIR_KEYPAD)
#   helpers.print_log_entries("third_dir_keypad_input :", third_dir_keypad_input, log_cats={"STEPS"})
#   return third_dir_keypad_input

def keep_shortest_ones (coll_set) :
  shortest_len = len(next(iter(coll_set)))
  for elem in coll_set :
    if len(elem) < shortest_len :
      shortest_len = len(elem)
  res_set = set()
  for elem in coll_set :
    if len(elem) == shortest_len :
      res_set.add(elem)
  return res_set

def get_shortest_one (coll_set) :
  chosen_elem = next(iter(coll_set))
  shortest_len = len(chosen_elem)
  for elem in coll_set :
    if len(elem) < shortest_len :
      chosen_elem = elem
      shortest_len = len(chosen_elem)
  return chosen_elem

def keep_shortest_poss (new_rep) :
  res_list = []
  for e in new_rep :
    res_list.append(keep_shortest_ones(e))
  return res_list

def process_code_v2 (num_keypad_input) :
  first_dir_keypad_inputs = keep_shortest_ones(process_code_aux_v2(num_keypad_input, BUTTON_POSITIONS_NUM_KEYPAD))
  second_dir_keypad_inputs = set()
  for first_dir_in in first_dir_keypad_inputs :
    second_dir_keypad_inputs |= keep_shortest_ones(process_code_aux_v2(first_dir_in, BUTTON_POSITIONS_DIR_KEYPAD))
  third_dir_keypad_inputs = set()
  for second_dir_in in second_dir_keypad_inputs :
    third_dir_keypad_inputs |= keep_shortest_ones(process_code_aux_v2(second_dir_in, BUTTON_POSITIONS_DIR_KEYPAD))
  # return first_dir_keypad_inputs
  # return second_dir_keypad_inputs
  return keep_shortest_ones(third_dir_keypad_inputs)

def rev_code_aux(code, pos_dict) :
  pos_row, pos_col = pos_dict[PRESS_CHAR]
  rev_dict = dict()
  for key, pos in pos_dict.items() :
    rev_dict[pos] = key
  res = ""
  for c in code :
    if c == PRESS_CHAR :
      if (pos_row, pos_col) in rev_dict :
        res += rev_dict[(pos_row, pos_col)]
      else :
        raise Exception("{} not in rev_dict ! (res currently at : {})".format((pos_row, pos_col), res))
    else :
      dir_row, dir_col = ALL_DIRS[c]
      pos_row += dir_row
      pos_col += dir_col
  return res

def rev_code(code) :
  helpers.print_log_entries("{}".format(code), log_cats={"I"})
  typed_on_second_dir = rev_code_aux(code, BUTTON_POSITIONS_DIR_KEYPAD)
  helpers.print_log_entries("{}".format(typed_on_second_dir), log_cats={"I"})
  typed_on_first_dir = rev_code_aux(typed_on_second_dir, BUTTON_POSITIONS_DIR_KEYPAD)
  helpers.print_log_entries("{}".format(typed_on_first_dir), log_cats={"I"})
  typed_on_num = rev_code_aux(typed_on_first_dir, BUTTON_POSITIONS_NUM_KEYPAD)
  helpers.print_log_entries("{}".format(typed_on_num), log_cats={"I"})
  return typed_on_num

# def compute_complexity (num_keypad_input) :
#   input_num_part = int(re.sub("[^0-9]", "", num_keypad_input))
#   shortest_output = process_code(num_keypad_input)
#   return input_num_part * len(shortest_output)

def compute_complexity_v2 (num_keypad_input) :
  input_num_part = int(re.sub("[^0-9]", "", num_keypad_input))
  shortest_outputs = process_code_v2(num_keypad_input)
  some_output = next(iter(shortest_outputs))
  return (some_output, input_num_part * len(some_output))

helpers.LOG_DICT["T"][0] = True
# helpers.LOG_DICT["STEPS"] = [True]

helpers.LOG_DICT["D"][0] = True

total_test_complexity = 0
for test_code in le_test_lines :
  test_output, curr_test_complexity = compute_complexity_v2(test_code)
  helpers.print_log_entries("Output for {} :\n{}\n(len {})".format(test_code, test_output, len(test_output)), log_cats={"R"})
  helpers.print_log_entries("Complexity for {} : {}".format(test_code, curr_test_complexity), log_cats={"R"})
  total_test_complexity += curr_test_complexity
helpers.print_log_entries("\n", log_cats={"R"})


helpers.print_log_entries("Total test complexity : {}".format(total_test_complexity), log_cats={"T"})

rev_code(compute_complexity_v2("379A")[0])
rev_code("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

# "^A<<^^A>>AvvvA" in process_code_aux_v2("379A", BUTTON_POSITIONS_NUM_KEYPAD)
# "<A>Av<<AA>^AA>AvAA^A<vAAA>^A" in process_code_aux_v2("^A<<^^A>>AvvvA", BUTTON_POSITIONS_DIR_KEYPAD)
# "<vA>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A" in process_code_aux_v2("<A>Av<<AA>^AA>AvAA^A<vAAA>^A", BUTTON_POSITIONS_DIR_KEYPAD)
# "v<<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>Av<<A>A>^AAAvA<^A>A" in process_code_aux_v2("<A>Av<<AA>^AA>AvAA^A<vAAA>^A", BUTTON_POSITIONS_DIR_KEYPAD)

total_complexity = 0
for code in le_lines :
  output, curr_complexity = compute_complexity_v2(code)
  helpers.print_log_entries("Output for {} :\n{}\n(len {})".format(code, output, len(output)), log_cats={"R"})
  helpers.print_log_entries("Complexity for {} : {}".format(code, curr_complexity), log_cats={"R"})
  total_complexity += curr_complexity
helpers.print_log_entries("\n", log_cats={"R"})

helpers.print_log_entries("Total complexity : {}".format(total_complexity), log_cats={"R"})

# print(process_code_v2("029A"))

######
# PART 2
######

# def get_ctc_rep(word_str, prev_char = PRESS_CHAR) :
#   wrd_len = 0
#   ctc_dict = dict()
#   for curr_char in word_str :
#     wrd_len += 1
#     if prev_char != curr_char :
#       curr_pair = (prev_char, curr_char)
#       if curr_pair in ctc_dict :
#         ctc_dict[curr_pair] += 1
#       else :
#         ctc_dict[curr_pair] = 1
#       prev_char = curr_char
#   ctc_dict["len"] = wrd_len
#   return ctc_dict

# def compute_hint(ctc_pair, pos_dict = BUTTON_POSITIONS_DIR_KEYPAD, max_step_count = 25) :
#   """
#   See if there are two paths possible from prev_char to next_char
#   If yes, find out which choice is the most beneficial, by finding next possible ctc_reps
#   for each (with max_step_count iterations at most), and seeing which one results in
#   the shortest code length
#   If max_step_count is reached before a better choice is determined, return None ?
#   """
#   prev_char, next_char = ctc_pair
#   prev_pos = pos_dict[prev_char]
#   next_pos = pos_dict[next_char]
#   moves_dict = compute_moves_pos(prev_pos, next_pos)
#   moves_count = len(moves_dict)
#   g_row, g_col = NO_POS
#   prev_row, prev_col = prev_pos
#   curr_row, curr_col = next_pos
#   if GAP_CHAR in pos_dict :
#     g_row, g_col = pos_dict[GAP_CHAR]
#   if prev_row == g_row and curr_col == g_col :
#     _orderings = remove_if_starts_with(_orderings, set("><"))
#     pass
#   elif prev_col == g_col and curr_row == g_row :
#     _orderings = remove_if_starts_with(_orderings, set("^v"))
#     pass
#   if len(_orderings) == 0 :
#     raise Exception("compute_hint() error : there should be at least one ordering(s) !")
#   elif len(_orderings) == 1 :
#     return next(iter(_orderings))
#   elif len(_orderings) > 2 :
#     raise Exception("compute_hint() error : there should be at most two ordering(s) !")
#   else :
#     orderings_list = list(_orderings)
#     fst_ordering, snd_ordering = fst_ordering, orderings_list[1]
#     ctc_dict_0 = {
#       (prev_char, fst_ordering[0]) : 1,
#       (fst_ordering[0], fst_ordering[1]) : 1,
#       (fst_ordering[1], PRESS_CHAR) : 1,
#       "len" : moves_dict[fst_ordering[0]] + moves_dict[fst_ordering[1]] + 1
#     }
#     ctc_dict_1 = {
#       (prev_char, snd_ordering[0]) : 1,
#       (snd_ordering[0], snd_ordering[1]) : 1,
#       (snd_ordering[1], PRESS_CHAR) : 1,
#       "len" : moves_dict[snd_ordering[0]] + moves_dict[snd_ordering[1]] + 1
#     }
#     for i in range(max_step_count) :
#       pass
#   for _ordering in get_orderings(moves_dict) :
#     pass
#   pass

# def process_ctc_pair(ctc_pair, pos_dict = BUTTON_POSITIONS_DIR_KEYPAD) :
#   prev_char, next_char = ctc_pair
#   prev_pos = pos_dict[prev_char]
#   next_pos = pos_dict[next_char]
#   next_rep_set = set()
#   moves_dict = compute_moves_pos(prev_pos, next_pos)
#   g_row, g_col = NO_POS
#   prev_row, prev_col = prev_pos
#   curr_row, curr_col = next_pos
#   if GAP_CHAR in pos_dict :
#     g_row, g_col = pos_dict[GAP_CHAR]
#   _orderings = get_orderings(moves_dict)
#   if prev_row == g_row and curr_col == g_col :
#     _orderings = remove_if_starts_with(_orderings, set("><"))
#   elif prev_col == g_col and curr_row == g_row :
#     _orderings = remove_if_starts_with(_orderings, set("^v"))
#   # ?
#   pass
  

# def compute_next_rep_set(ctc_dict_set, pos_dict = BUTTON_POSITIONS_DIR_KEYPAD, prev_char = PRESS_CHAR) :
#   for ctc_dict in ctc_dict_set :
#     for ctc_pair in ctc_dict :
#       pass

# helpers.LOG_DICT["ITER"] = [True]

# total_complexity_with_25_dir = 0
# for code in le_lines :
#   output_with_25_dir, curr_complexity_with_25_dir = compute_complexity_with_25_dir(code)
#   helpers.print_log_entries("Output for {} :\n{}\n(len {})".format(code, output_with_25_dir, len(output_with_25_dir)), log_cats={"R"})
#   helpers.print_log_entries("Complexity for {} : {}".format(code, curr_complexity_with_25_dir), log_cats={"R"})
#   total_complexity_with_25_dir += curr_complexity_with_25_dir
# helpers.print_log_entries("\n", log_cats={"R"})

# helpers.print_log_entries("Total complexity : {}".format(total_complexity_with_25_dir), log_cats={"R"})

def process_code_aux_v3 (code_str, pos_dict, prev_char = PRESS_CHAR) :
  """
  Process code to find resulting code/moves, i.e. that, when put into a robot on a keypad
  will make it "type out" code_str
  """
  res_codes_temp = set()
  g_row, g_col = NO_POS
  if GAP_CHAR in pos_dict :
    g_row, g_col = pos_dict[GAP_CHAR]
  if len(code_str) > 0 :
    res = ""
    for i in range(len(code_str)) :
      prev_pos = pos_dict[prev_char]
      prev_row, prev_col = prev_pos
      curr_char = code_str[i]
      curr_pos = pos_dict[curr_char]
      curr_row, curr_col = curr_pos
      #
      next_moves_dict = dict()
      _orderings = set()
      next_moves_dict = compute_moves_pos(prev_pos, curr_pos)
      _orderings = get_orderings(next_moves_dict)
      # remove orderings that would make robot go over gap
      if prev_row == g_row and curr_col == g_col :
        _orderings = remove_if_starts_with(_orderings, set("><"))
        pass
      elif prev_col == g_col and curr_row == g_row :
        _orderings = remove_if_starts_with(_orderings, set("^v"))
        pass
      # Keep better orderings
      better_orderings = set()
      for ordering in _orderings :
        if len(ordering) > 1 and ordering[0] == "<" :
          continue
        else :
          better_orderings.add(ordering)
      #
      if (len(better_orderings) > 0) :
        _orderings = better_orderings
      res += "".join([move * next_moves_dict[move] for move in ordering]) + PRESS_CHAR
      prev_char = code_str[i]
    return res
    # return res_code_temp + process_code_aux_v3(code_str[1:], pos_dict, curr_char)
    # for ordering in _orderings :
    #   res_codes_temp.add("".join([move * next_moves_dict[move] for move in ordering]) + PRESS_CHAR)
    # res_codes = set()
    # for tmp_code_head in res_codes_temp :
    #   for tmp_code_rest in process_code_aux_v3(code_str[1:], pos_dict, curr_char) :
    #     res_codes.add(tmp_code_head + tmp_code_rest)
    # return keep_shortest_ones(res_codes)
  else :
    return ""
    # return {""}

def process_code_v3 (num_keypad_input) :
  # next_input = next(iter(process_code_aux_v3(num_keypad_input, BUTTON_POSITIONS_NUM_KEYPAD)))
  # for i in range(25) :
  #   next_input = next(iter(process_code_aux_v3(next_input, BUTTON_POSITIONS_DIR_KEYPAD)))
  # return next_input
  next_input = process_code_aux_v3(num_keypad_input, BUTTON_POSITIONS_NUM_KEYPAD)
  for i in range(25) :
    print("Currently at iteration n°{}".format(i))
    next_input = process_code_aux_v3(next_input, BUTTON_POSITIONS_DIR_KEYPAD)
  return next_input

# process_code_v3("379A")

def produce_move(keypair, pos_dict) :
  """
  Turns keypair into string of characters corresponding to the keys
  that need to be pressed on a directional keypad to move from first
  key of keypair over to second key of keypair
  """
  #
  prev_char, curr_char = keypair
  prev_pos = pos_dict[prev_char]
  prev_row, prev_col = prev_pos
  curr_pos = pos_dict[curr_char]
  curr_row, curr_col = curr_pos
  #
  next_moves_dict = dict()
  _orderings = set()
  next_moves_dict = compute_moves_pos(prev_pos, curr_pos)
  _orderings = get_orderings(next_moves_dict)
  # 
  g_row, g_col = NO_POS
  if GAP_CHAR in pos_dict :
    g_row, g_col = pos_dict[GAP_CHAR]
  # remove orderings that would make robot go over gap
  if prev_row == g_row and curr_col == g_col :
    _orderings = remove_if_starts_with(_orderings, set("><"))
    pass
  elif prev_col == g_col and curr_row == g_row :
    _orderings = remove_if_starts_with(_orderings, set("^v"))
    pass
  # Keep better ordering (one that starts with "<", if it exists)
  # This is very important, but I don't feel like explaining in length why it should work here
  better_ordering = next(iter(_orderings))
  for ordering in _orderings :
    if len(ordering) > 0 :
      if ordering[0] == '<' :
        better_ordering = ordering
  return "".join([move * next_moves_dict[move] for move in better_ordering])

def str_to_keypairs_dict(code_str, prev_char = PRESS_CHAR) :
  """
  Turns any string into a dict containing all pairs of consecutive distinct
  keys [chars] as keys [dict keys], and the number of times they occur as values
  """
  press_count = 0
  res_dict = {}
  for next_char in code_str :
    # if prev_char != next_char :
    if True :
      keypair = (prev_char, next_char)
      if keypair not in res_dict :
        res_dict[keypair] = 0
      res_dict[keypair] += 1
    press_count += 1
    #
    prev_char = next_char
  return res_dict

def process_code_aux_v4 (keypairs_dict, pos_dict) :
  """
  Process code to find resulting code/moves, i.e. that, when put into a robot on a keypad
  will make it "type out" code_str
  """
  helpers.print_log_entries("aux_v4 - got called with dict {}".format(keypairs_dict), log_cats={"D"})
  res_dict = dict()
  press_count = 0
  for keypair, keypair_count in keypairs_dict.items() :
    move_and_press_addition = produce_move(keypair, pos_dict) + PRESS_CHAR
    press_count += len(move_and_press_addition) * keypair_count
    for addition_keypair, addition_keypair_count in str_to_keypairs_dict(move_and_press_addition).items() :
      if addition_keypair not in res_dict :
        res_dict[addition_keypair] = 0
      res_dict[addition_keypair] += keypair_count * addition_keypair_count
  # small check
  check_sum = 0
  for key, val in res_dict.items() :
    check_sum += val
  if check_sum != press_count :
    raise RuntimeError("process_code_aux_v4() error : bad checksum !")
  return res_dict, press_count

def process_code_v4 (code_str) :
  next_keypairs_dict = str_to_keypairs_dict(code_str)
  next_press_count = len(code_str)
  next_keypairs_dict, next_press_count = process_code_aux_v4(next_keypairs_dict, BUTTON_POSITIONS_NUM_KEYPAD)
  for i in range(25) :
    helpers.print_log_entries("Currently at iteration n°{}".format(i), log_cats = {"D"})
    next_keypairs_dict, next_press_count = process_code_aux_v4(next_keypairs_dict, BUTTON_POSITIONS_DIR_KEYPAD)
  return next_press_count

def compute_complexity_v4(code_str) :
  input_num_part = int(re.sub("[^0-9]", "", code_str))
  shortest_output_length = process_code_v4(code_str)
  return input_num_part * shortest_output_length

def find_total_complexity_v4(lines) :
  total_complexity = 0
  for code_str in lines :
    curr_complexity = compute_complexity_v4(code_str)
    helpers.print_log_entries("Complexity for {} : {}".format(code_str, curr_complexity), log_cats={"R"})
    total_complexity += curr_complexity
  helpers.print_log_entries("\n", log_cats={"R"})
  # helpers.print_log_entries("Total complexity : {}".format(total_complexity), log_cats={"R"})
  return total_complexity

helpers.LOG_DICT["D"][0] = False

helpers.print_log_entries("", "Total complexity when we have 25 (TWENTY-FIVE !) directional"
                          " keyboards :", find_total_complexity_v4(le_lines), log_cats= {"R"})