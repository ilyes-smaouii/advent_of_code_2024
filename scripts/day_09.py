import helpers

# open file, collect content
le_filename = "../inputs/day_09_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()
# le_file_content = """00...111...2...333.44.5555.6666.777.888899""" # [testing]
# le_file_content = """2333133121414131402""" # [testing]

######
# PART 1
######

POINT_REP = -1

def get_blocks_rep(disk_map) :
  blocks = []
  curr_id = 0
  is_empty = False
  for i in range(0, len(disk_map)) :
    if not is_empty :
      blocks += [curr_id] * disk_map[i]
      curr_id += 1
    else :
      blocks += [POINT_REP] * disk_map[i]
    is_empty = not is_empty
  return blocks

def fs_to_str(blocks_rep) :
  return "".join(str(elem) if elem != POINT_REP else "." for elem in blocks_rep)

def compress_filesystem(blocks_rep) :
  right_cursor_idx = len(blocks_rep) - 1
  left_cursor_idx = 0
  while left_cursor_idx < right_cursor_idx :
    if right_cursor_idx - left_cursor_idx % 1 == 0 :
      print("right_cursor_idx - left_cursor_idx = ", right_cursor_idx - left_cursor_idx, sep = "") # [debugging]
    do_swap = True
    if blocks_rep[left_cursor_idx] != POINT_REP :
      left_cursor_idx += 1
      do_swap = False
    if blocks_rep[right_cursor_idx] == POINT_REP :
      right_cursor_idx -= 1
      do_swap = False
    if do_swap :
      blocks_rep[left_cursor_idx], blocks_rep[right_cursor_idx] = \
        blocks_rep[right_cursor_idx], blocks_rep[left_cursor_idx]
  return blocks_rep

def compute_checksum(blocks_rep) :
  final_checksum = 0
  for i in range(len(blocks_rep)) :
    if (blocks_rep[i] == POINT_REP) :
      continue
    final_checksum += (i * blocks_rep[i])
  return final_checksum

def fs_to_str_v2(blocks_rep) :
  return "".join(blocks_rep)

def compress_filesystem_v2(disk_map_str) :
  right_cursor_idx = len(disk_map_str) - 1
  left_cursor_idx = 0
  while left_cursor_idx < right_cursor_idx :
    if right_cursor_idx - left_cursor_idx % 1 == 0 :
      print("right_cursor_idx - left_cursor_idx = ", right_cursor_idx - left_cursor_idx, sep = "") # [debugging]
    do_swap = True
    if disk_map_str[left_cursor_idx] != "." :
      left_cursor_idx += 1
      do_swap = False
    if disk_map_str[right_cursor_idx] == "." :
      right_cursor_idx -= 1
      do_swap = False
    if do_swap :
      disk_map_str[left_cursor_idx], disk_map_str[right_cursor_idx] = \
        disk_map_str[right_cursor_idx], disk_map_str[left_cursor_idx]
  return disk_map_str

def compute_checksum_v2(blocks_rep) :
  final_checksum = 0
  for i in range(len(blocks_rep)) :
    if (blocks_rep[i] == ".") :
      continue
    final_checksum += (i * int(blocks_rep[i]))
  return final_checksum

le_disk_map = [int(elem) if elem != "." else POINT_REP for elem in le_file_content]
le_disk_map_str = [elem for elem in le_file_content]
print("got blocks_rep", sep = "") # [debugging]

print("getting map, then compressing :\n", helpers.concat_table_as_str(le_disk_map), "\n", fs_to_str(get_blocks_rep(le_disk_map)), \
  "\n",
  fs_to_str(compress_filesystem(get_blocks_rep(le_disk_map))), sep = "") # [testing]

print("Compressed filesystem's checkum : ", compute_checksum(compress_filesystem(get_blocks_rep(le_disk_map))))

######
# PART 2
######