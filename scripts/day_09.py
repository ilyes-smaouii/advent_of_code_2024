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

le_disk_map = [int(elem) if elem != "." else POINT_REP for elem in le_file_content]
le_disk_map_str = [elem for elem in le_file_content]
print("got blocks_rep", sep = "") # [debugging]

# print("getting map, then compressing :\n", helpers.concat_table_as_str(le_disk_map), "\n", fs_to_str(get_blocks_rep(le_disk_map)), \
#   "\n",
#   fs_to_str(compress_filesystem(get_blocks_rep(le_disk_map))), sep = "") # [testing]

print("Compressed filesystem's checkum : ", compute_checksum(compress_filesystem(get_blocks_rep(le_disk_map))))

# TO-DO : clean up part 1 code ?

######
# PART 2
######

def disk_map_to_ranges_rep(disk_map) :
  file_ranges = []
  empty_ranges = []
  file_or_empty = 1 # 1 for file, 0 for empty
  curr_file_id = 0
  curr_idx = 0
  for elem in disk_map :
    if file_or_empty == 1 :
      file_ranges.append((elem, curr_idx, curr_file_id))
      curr_file_id += 1
    else :
      empty_ranges.append((elem, curr_idx, POINT_REP))
      pass
    file_or_empty = 1 - file_or_empty
    curr_idx += elem
  return file_ranges, empty_ranges

def get_checksum_for_compressed_disk_map_defrag(disk_map) :
  file_ranges, empty_ranges = disk_map_to_ranges_rep(disk_map)
  # print("file_ranges, empty_ranges :\n", file_ranges, "\n", empty_ranges, sep = "") # [debugging]
  compressed_file_ranges = []
  # print("compressed_file_ranges :\n", compressed_file_ranges, sep = "") # [debugging]
  for file_size, file_pos, file_id in reversed(file_ranges) :
    has_been_compressed = False
    for em_idx in range(len(empty_ranges)) :
      if empty_ranges[em_idx][1] > file_pos :
        continue
      if empty_ranges[em_idx][0] == file_size :
        compressed_file_ranges.append((file_size, empty_ranges[em_idx][1], file_id))
        empty_ranges.remove(empty_ranges[em_idx])
        has_been_compressed = True
        break
      elif empty_ranges[em_idx][0] > file_size :
        compressed_file_ranges.append((file_size, empty_ranges[em_idx][1], file_id))
        empty_ranges[em_idx] = (empty_ranges[em_idx][0] - file_size, empty_ranges[em_idx][1] + file_size, empty_ranges[em_idx][2])
        has_been_compressed = True
        break
      else :
        continue
    if not has_been_compressed :
      compressed_file_ranges.append((file_size, file_pos, file_id))
  # print("compressed_file_ranges (after) :\n", compressed_file_ranges, sep = "") # [debugging]
  # Now we loop on compressed_file_ranges to compute checksum
  checksum = 0
  for file_size, file_pos, file_id in compressed_file_ranges :
    checksum += file_id * file_size * (file_pos + (file_pos + file_size - 1))/2
  return checksum

print("Compressed (no frag) filesystem's checkum : ", get_checksum_for_compressed_disk_map_defrag(le_disk_map))
