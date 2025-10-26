import helpers

# open file, collect content
le_filename = "../inputs/day_25_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
# le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)

######
# PART 1
######

KEY_AND_LOCK_DEPTH = 5
OCCUPIED_CHAR = '#'
EMPTY_CHAR = '.'

le_keys_and_locks_str = le_file_content.split("\n\n")

le_keys = set()
le_locks = set()

for key_or_lock_str in le_keys_and_locks_str:
  lines = key_or_lock_str.split("\n")
  cols = []
  for i in range(KEY_AND_LOCK_DEPTH):
    cols.append(
      len([line[i] for line in lines if line[i] == OCCUPIED_CHAR]) - 1)
  if lines[0] == EMPTY_CHAR * KEY_AND_LOCK_DEPTH and lines[-1] == OCCUPIED_CHAR * KEY_AND_LOCK_DEPTH:
    le_keys.add(tuple(cols))
  elif lines[0] == OCCUPIED_CHAR * KEY_AND_LOCK_DEPTH and lines[-1] == EMPTY_CHAR * KEY_AND_LOCK_DEPTH:
    le_locks.add(tuple(cols))
  else:
    raise RuntimeError("Parsing error : each block should be a key or a ")


def key_fits_in_lock(key, lock):
  for i in range(KEY_AND_LOCK_DEPTH):
    if key[i] + lock[i] > 5:
      return False
  return True


def count_fitting_pairs(keys, locks):
  pair_count = 0
  for key in keys:
    for lock in locks:
      if key_fits_in_lock(key, lock):
        pair_count += 1
  return pair_count


helpers.set_log_by_parts()

le_pair_count = count_fitting_pairs(le_keys, le_locks)

helpers.print_log_entries(
  "Number of unique lock/key pairs that fit together without overlapping in any column :", le_pair_count, log_cats={"R"})

######
# PART 2
######
